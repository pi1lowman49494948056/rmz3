#include "collision.h"
#include "gfx.h"
#include "global.h"
#include "motion.h"
#include "overworld.h"
#include "score.h"
#include "script.h"
#include "sound.h"
#include "stagerun.h"
#include "weapon.h"

/* Shield input/charge/release stays in Zero's original state machine.
 * Do not count R presses independently: main/sub mappings and charge completion
 * belong to the player. CreateWeaponShieldFly is its charged-shot dispatch.
 */
#define BOW_ARROW_LIFE 0x50
static void BowCharge_Init(struct Weapon* p);
static void BowArrow_Init(struct Weapon* p);
static void BowArrow_Update(struct Weapon* p);
static void BowArrow_Die(struct Weapon* p);
static void BowArrow_Hit(struct Body* body, Coords32* a, Coords32* b);

// ---------------------------------------------------------------------------
// DSH demo: position trigger -> native teleport cutscene (minimal validation).
// The stage-update hook watches Zero's position, starts the teleport script
// when he reaches the trigger column, and snaps his X during the teleport's
// invisible window (between force 5 and force 6).

#include "dsh_room_config.h"

static u8 sDshPhase;        // 0=idle 1=waiting to start 2=running 3=done
static u16 sDshWait;

// Dialogue text as raw charmap bytes (no preproc needed).  text_window.c
// repoints table 19 (TB_OTHERS) to these.  TextIDs: 0x1300 = Ciel, 0x1301 = Zero.
//   {WINDOW 0x40} = mugshot 32 (Ciel) left
//   {WINDOW 0x05} = mugshot 2  (Zero) right
const u8 gDshTexts[] = {
    // Ciel: "ZERO, TEST THE BOW."
    0xF3, 0x40,
    0x24, 0x0F, 0x1C, 0x19, 0xD5, 0x00,   // ZERO,
    0x1E, 0x0F, 0x1D, 0x1E, 0x00,         // TEST
    0x1E, 0x12, 0x0F, 0x00,               // THE
    0x0C, 0x19, 0x21, 0xE5,               // BOW.
    0xFF,                                 // $
    // Zero: "UNDERSTOOD."
    0xF3, 0x05,
    0x1F, 0x18, 0x0E, 0x0F, 0x1C, 0x1D, 0x1E, 0x19, 0x19, 0x0E, 0xE5,  // UNDERSTOOD.
    0xFF,                                 // $
};

const u16 gDshTextOfs[] = { 0, 22 };

// Each short script leaves control locked until the complete transfer finishes.
static const GameCommand gDshTeleportScript[] = {
  {.c = {.op = 0x09, .status = 0, .val2 = 0, .work = 0}},
  {.c = {.op = 0x17, .status = 0, .val2 = 0, .work = 4864}},
  {.c = {.op = 0x17, .status = 2, .val2 = 0, .work = 0}},
  {.c = {.op = 0x17, .status = 0, .val2 = 0, .work = 4865}},
  {.c = {.op = 0x17, .status = 2, .val2 = 0, .work = 0}},
  {.c = {.op = 0x1a, .status = 1, .val2 = 0, .work = 0}},
  {.c = {.op = 0x1a, .status = 4, .val2 = 0, .work = 0}},
  {.c = {.op = 0xff, .status = 0, .val2 = 0, .work = 0}},
};
static const GameCommand gDshDisappear[] = {
  {.c = {.op = 0x1a, .status = 5, .val2 = 0, .work = 0}},
  {.c = {.op = 0xff, .status = 0, .val2 = 0, .work = 0}},
};
static const GameCommand gDshBlackout[] = {
  {.c = {.op = 0x14, .status = 2, .val2 = 0, .work = 0}},
  {.c = {.op = 0x14, .status = 0, .val2 = 0, .work = 0}},
  {.c = {.op = 0xff, .status = 0, .val2 = 0, .work = 0}},
};
static const GameCommand gDshArrival[] = {
  {.c = {.op = 0x1a, .status = 6, .val2 = 0, .work = 0}},
  {.c = {.op = 0x14, .status = 1, .val2 = 0, .work = 0}},
  {.c = {.op = 0x14, .status = 0, .val2 = 0, .work = 0}},
  {.c = {.op = 0x1a, .status = 7, .val2 = 0, .work = 0}},
  {.c = {.op = 0x09, .status = 1, .val2 = 0, .work = 0}},
  {.c = {.op = 0xff, .status = 0, .val2 = 0, .work = 0}},
};
void DshStageUpdate(Coords32* c UNUSED);

static const struct Collision sBowArrowCollision = {
  kind : DDP, faction : FACTION_ALLY, special : HALFABLE,
  damage : 6, atkType : ATK_NORMAL, comboLv : 2,
  remaining : 0, layer : 0x00000020,
  range : {PIXEL(0), PIXEL(0), PIXEL(14), PIXEL(8)},
};

const WeaponRoutine gDshBowChargeRoutine = {
  [ENTITY_INIT] = (void*)BowCharge_Init,
  [ENTITY_UPDATE] = (void*)BowCharge_Init,
  [ENTITY_DIE] = (void*)DeleteWeapon,
  [ENTITY_DISAPPEAR] = (void*)DeleteWeapon,
  [ENTITY_EXIT] = (void*)DeleteEntity,
};
const WeaponRoutine gDshBowShotRoutine = {
  [ENTITY_INIT] = (void*)BowArrow_Init,
  [ENTITY_UPDATE] = (void*)BowArrow_Update,
  [ENTITY_DIE] = (void*)BowArrow_Die,
  [ENTITY_DISAPPEAR] = (void*)DeleteWeapon,
  [ENTITY_EXIT] = (void*)DeleteEntity,
};

static void BowCharge_Init(struct Weapon* p) {
  /* No shield guard hitbox or persistent charge entity. Zero owns charging. */
  (p->s).flags &= ~(DISPLAY | FLIPABLE);
  EXIT_BODY(p);
  SET_WEAPON_ROUTINE(p, ENTITY_EXIT);
}

static void BowArrow_Init(struct Weapon* p) {
  struct Zero* z = ((struct WeaponCommon*)p)->props.z;
  bool8 right;
  if (z == NULL || (z->body).hp == 0) {
    BowArrow_Die(p);
    return;
  }
  right = ((z->s).flags & X_FLIP) != 0;
  if ((z->s).mode[1] == ZERO_WALL) right = !right;
  InitNonAffineMotion(&p->s);
  ResetDynamicMotion(&p->s);
  (p->s).flags |= DISPLAY | FLIPABLE;
  /* Supplied artwork points left, matching the default sprite direction. */
  SET_XFLIP(p, right);
  SET_YFLIP(p, FALSE);
  (p->s).coord = (z->s).coord;
  (p->s).coord.x += right ? PIXEL(16) : -PIXEL(16);
  (p->s).coord.y -= PIXEL(18);
  (p->s).d.x = right ? PIXEL(6) : -PIXEL(6);
  (p->s).d.y = 0;
  (p->s).work[2] = BOW_ARROW_LIFE;
  (p->s).work[3] = 0;
  /* DM109 belongs to shield flight; DM136 must remain the Buster's. */
  SetSpriteAnimation(p, MOTION(DM109_UNK, 0));
  INIT_BODY(p, &sBowArrowCollision, 1, BowArrow_Hit);
  SET_WEAPON_ROUTINE(p, ENTITY_UPDATE);
  PlaySound(SE_CHARGE_SHIELD_VOICE);
  UpdateSpriteAnimation(p);
}

static void BowArrow_Hit(struct Body* body, Coords32* a UNUSED, Coords32* b UNUSED) {
  if (body->hitboxFlags & (BODY_STATUS_B2 | BODY_STATUS_BLOCKED)) {
    struct Weapon* p = (struct Weapon*)body->parent;
    (p->s).work[3] = 1;
    IncWeaponUseCount(WEAPON_SHIELD);
  }
}

static void BowArrow_Update(struct Weapon* p) {
  if ((p->s).work[3] || ((p->body).status & BODY_STATUS_BLOCKED) || !(p->s).work[2]) {
    BowArrow_Die(p);
    return;
  }
  (p->s).work[2]--;
  (p->s).coord.x += (p->s).d.x;
  UpdateSpriteAnimation(p);
}

static void BowArrow_Die(struct Weapon* p) {
  (p->s).flags &= ~(DISPLAY | FLIPABLE);
  EXIT_BODY(p);
  SET_WEAPON_ROUTINE(p, ENTITY_EXIT);
}

// Keep retail checkpoint-3 initialization, but never run its later mission events.
s16 DshMissionUpdate(struct StageRun* p) {
  if (p->stageEventPhase == 0) {
    sDshPhase = 0;
    sDshWait = 0;
    gInTransport = FALSE;
    p->checkpoint = 3;
    return SpaceCraft_MissionUpdate(p);
  }
  return 0;
}

// Scope index 14 to the normal Zero palette while displaying the bow pose.
// Do not replace damage/charge flash palettes or unrelated original resources.
static bool8 sDshBowGreen;
static u16 sDshBowPaletteIndex;
static u16 sDshBowOriginalColor;
static u16 sDshBowWrittenColor;
static void DshUpdateBowPalette(struct Zero* z) {
  u16 index = z != NULL ? 256 + (z->s.palID & 15) * 16 + 14 : 0;
  bool8 bow = z != NULL && z->body.hp != 0 &&
              (z->s.motionID == DM040_ZERO_SHIELD_GUARD || z->s.motionID == DM043_ZERO_SHIELD_AIR);
  u16* color;
  if (sDshBowGreen && (!bow || index != sDshBowPaletteIndex)) {
    color = &gPaletteManager.buf[sDshBowPaletteIndex];
    if (*color == sDshBowWrittenColor) *color = sDshBowOriginalColor;
    sDshBowGreen = FALSE;
  }
  if (!bow) return;
  color = &gPaletteManager.buf[index];
  // Zero's normal palette stores dark green as 0x95AB, not 0x15AB.
  // Preserve the engine's high bit; do not overwrite a flash/alternate color.
  if ((*color & 0x7FFF) == 0x15AB) {
    sDshBowPaletteIndex = index;
    sDshBowOriginalColor = *color;
    sDshBowWrittenColor = (*color & 0x8000) | 0x3FF2;
    *color = sDshBowWrittenColor;
    sDshBowGreen = TRUE;
  }
}

void DshStageUpdate(Coords32* c UNUSED) {
  struct Zero* z = (struct Zero*)gStageRun.vm.entities[0].entity;
  struct Camera* cam = &gStageRun.vm.camera;
  DshUpdateBowPalette(z);
  if (z == NULL || z->body.hp == 0) return;
  if (gStageRun.vm.active & VM_ACTIVE) return;
  switch (sDshPhase) {
    case 0:
      if ((z->s).coord.x >= PIXEL(DSH_TRIGGER_X) &&
          (z->s).coord.x < PIXEL(DSH_ROOM_RIGHT) &&
          (z->s).coord.y >= PIXEL(DSH_ROOM_TOP) &&
          (z->s).coord.y < PIXEL(DSH_ROOM_BOTTOM) &&
          (z->s).mode[1] == ZERO_GROUND) {
        (z->s).d.x = (z->s).d.y = 0;
        gStageRun.missionStatus |= DISABLE_MENU;
        SetScript(&gStageRun.vm, gDshTeleportScript);
        sDshPhase = 1;
      }
      break;
    case 1:
      if ((z->s).mode[1] == ZERO_TELEPORT && (z->s).mode[2] == 2 &&
          (z->s).mode[3] == 2 && (z->s).motion.state == ANIM_NEXT_GOTO) {
        SetScript(&gStageRun.vm, gDshDisappear);
        sDshPhase = 2;
      }
      break;
    case 2:
      if ((z->s).mode[2] == 3 && (z->s).mode[3] == 2 &&
          !((z->s).flags & DISPLAY)) {
        SetScript(&gStageRun.vm, gDshBlackout);
        sDshPhase = 3;
      }
      break;
    case 3:
      (z->s).coord.x = PIXEL(DSH_TARGET_X);
      (z->s).coord.y = PIXEL(DSH_TARGET_Y) - 1;
      (z->s).d.x = (z->s).d.y = 0;
      cam->viewport.x = cam->target.x = PIXEL(DSH_TARGET_X);
      cam->viewport.y = cam->target.y = PIXEL(DSH_TARGET_CAMERA_Y);
      sDshWait = 0;
      sDshPhase = 4;
      break;
    case 4:
      // Allow terrain/background transfers to settle while the screen is black.
      if (++sDshWait >= 4) {
        SetScript(&gStageRun.vm, gDshArrival);
        sDshPhase = 5;
      }
      break;
    case 5:
      gStageRun.missionStatus &= ~DISABLE_MENU;
      sDshPhase = 6; // once per room entry; retry resets through DshMissionUpdate
      break;
    default:
      break;
  }
}
