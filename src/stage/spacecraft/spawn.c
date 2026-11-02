#include "spawn.h"

#include "binary_literal.h"
#include "global.h"

// 0x08347a9c
const struct SpawnTemplate gSpaceCraftEntity[26] =
    {
        [0] = {0},
        [1] =
            {
                .flag = SF_FLAG_1,
                .kind = SpawnEntity(ENTITY_ITEM, ITEM_GENERAL, ITEM_LIFE_M, 2),
            },
        [2] =
            {
                .flag = SF_FLAG_1,
                .kind = SpawnEntity(ENTITY_ITEM, ITEM_GENERAL, ITEM_LIFE_L, 2),
            },
        [3] =
            {
                .flag = SF_FLAG_1,
                .kind = SpawnEntity(ENTITY_ITEM, ITEM_GENERAL, ITEM_EC_L, 2),
            },
        [4] =
            {
                .flag = SF_FLAG_1,
                .kind = SpawnEntity(ENTITY_ITEM, ITEM_GENERAL, ITEM_EXLIFE, 2),
            },
        [5] =
            {
                .flag = SF_RESPAWN,
                .kind = SpawnEntity(ENTITY_SOLID, SOLID_DOOR_2D_BLUE, 0, 0),
            },
        [6] =
            {
                .flag = SF_RESPAWN,
                .kind = SpawnEntity(ENTITY_SOLID, SOLID_DOOR_2D_BLUE, 2, 0),
            },
        [7] =
            {
                .flag = SF_RESPAWN,
                .kind = SpawnEntity(ENTITY_ENEMY, ENEMY_GRAND_CANNON, GRAND_CANNON_TURRET, 0),
                .attr = SA_KNIGHT,
                .mettaurID = 1,
                .virusID = VIRUS_BEETANK,
            },
        [8] =
            {
                .flag = SF_RESPAWN,
                .kind = SpawnEntity(ENTITY_ENEMY, ENEMY_SHRIMPORIN, 0, 0),
                .attr = SA_KNIGHT,
                .mettaurID = 1,
            },
        [9] =
            {
                .flag = SF_RESPAWN,
                .kind = SpawnEntity(ENTITY_ENEMY, ENEMY_SHRIMPORIN, 1, 0),
                .attr = SA_KNIGHT,
                .mettaurID = 1,
            },
        [10] =
            {
                .flag = SF_RESPAWN,
                .kind = SpawnEntity(ENTITY_ENEMY, ENEMY_P_HUNTER, 0, 0),
                .attr = SA_KNIGHT,
                .mettaurID = 1,
                .virusID = VIRUS_BEETANK,
            },
        [11] =
            {
                .flag = SF_RESPAWN,
                .kind = SpawnEntity(ENTITY_ENEMY, ENEMY_BATRING, 0, 0),
                .attr = SA_KNIGHT,
                .mettaurID = 2,
                .virusID = VIRUS_SWORDY,
            },
        [12] =
            {
                .flag = SF_RESPAWN,
                .kind = SpawnEntity(ENTITY_ENEMY, ENEMY_BATRING, 1, 0),
                .attr = SA_KNIGHT,
                .mettaurID = 2,
                .virusID = VIRUS_SWORDY,
            },
        [13] =
            {
                .flag = SF_RESPAWN,
                .kind = SpawnEntity(ENTITY_ENEMY, ENEMY_SHOTCOUNTER, 0, 0),
                .attr = SA_KNIGHT,
                .mettaurID = 2,
                .virusID = VIRUS_SWORDY,
            },
        [14] =
            {
                .flag = SF_RESPAWN,
                .kind = SpawnEntity(ENTITY_ENEMY, ENEMY_SHOTCOUNTER, 1, 0),
                .attr = SA_KNIGHT,
                .mettaurID = 2,
                .virusID = VIRUS_SWORDY,
            },
        [15] =
            {
                .flag = SF_RESPAWN,
                .kind = SpawnEntity(ENTITY_SOLID, SOLID_SCRIPT_ACTOR, 8, 0),
            },
        [16] =
            {
                .flag = SF_RESPAWN,
                .kind = SpawnEntity(ENTITY_SOLID, SOLID_ICE_BLOCK, 0, 0),
            },
        [17] =
            {
                .flag = SF_FLAG_1,
                .kind = SpawnEntity(ENTITY_ITEM, ITEM_DISK, 24, 2),
            },
        [18] =
            {
                .flag = SF_FLAG_1,
                .kind = SpawnEntity(ENTITY_ITEM, ITEM_DISK, 37, 2),
            },
        [19] =
            {
                .flag = SF_FLAG_1,
                .kind = SpawnEntity(ENTITY_ITEM, ITEM_DISK, 50, 2),
            },
        [20] =
            {
                .flag = SF_FLAG_1,
                .kind = SpawnEntity(ENTITY_ITEM, ITEM_DISK, 101, 2),
            },
        [21] =
            {
                .flag = SF_FLAG_1,
                .kind = SpawnEntity(ENTITY_SOLID, SOLID_CONTAINER, 2, 7),
            },
        [22] =
            {
                .flag = SF_FLAG_1,
                .kind = SpawnEntity(ENTITY_SOLID, SOLID_CONTAINER, 2, 111),
            },
        [23] =
            {
                .flag = SF_FLAG_1,
                .kind = SpawnEntity(ENTITY_SOLID, SOLID_CONTAINER, 2, 254),
            },
        [24] =
            {
                .flag = SF_FLAG_1,
                .kind = SpawnEntity(ENTITY_SOLID, SOLID_CONTAINER, 2, 255),
            },
        [25] =
            {
                .flag = 0xF,
                .kind = SpawnEntity(15, 255, 255, 255),
            },

};

const struct PreloadEntity gSpaceCraftStatic[8] = {
    {
        SM007_GRAND_CANNON,
        B8(00000001),
        512,
        4,
        1,
        1,
        0,
    },
    {
        SM013_SHRIMPOLIN,
        B8(00000001),
        553,
        5,
        1,
        3,
        0,
    },
    {
        SM019_PANTHEON_HUNTER,
        B8(00000001),
        681,
        6,
        1,
        1,
        0,
    },
    {
        SM006_BATRING,
        B8(00000001),
        801,
        7,
        1,
        1,
        0,
    },
    {
        SM004_SHOTCOUNTER,
        B8(00000001),
        898,
        8,
        1,
        1,
        0,
    },
    {
        SM203_ICE_BLOCK,
        B8(00000001),
        954,
        9,
        3,
        3,
        1,
    },
    {
        SM221_METTAUR,
        B8(01111111),
        512,
        6,
        2,
        3,
        0,
    },
    {
        255,
        255,
        4095,
        15,
        1,
        3,
        1,
    },
};

// 0x08347bac
// clang-format off
const struct SpawnPoint gSpaceCraftSpawnPoints[68] = {
	[0]  = { -0x80000000, -0x8000, 0 },
	// DSH demo: two Pantheon Hunters inside the test room (wall is at x=1680).
	[1]  = { SpawnPixelCoords(1500, 1680), 10 },
	[2]  = { SpawnPixelCoords(1650, 1680), 10 },
	[3]  = { SpawnPixelCoords(1968, 1696), 8 },
	[4]  = { SpawnPixelCoords(2256, 1616), 7 },
	[5]  = { SpawnPixelCoords(2320, 1616), 23 },
	[6]  = { SpawnPixelCoords(2384, 1552), 7 },
	[7]  = { SpawnPixelCoords(2480, 1536), 7 },
	[8]  = { SpawnPixelCoords(2544, 1456), 9 },
	[9]  = { SpawnPixelCoords(2768, 1568), 17 },
	[10] = { SpawnPixelCoords(2800, 1440), 8 },
	[11] = { SpawnPixelCoords(2992, 1376), 7 },
	[12] = { SpawnPixelCoords(3408, 1024), 16 },
	[13] = { SpawnPixelCoords(3408, 1088), 16 },
	[14] = { SpawnPixelCoords(3424, 384), 10 },
	[15] = { SpawnPixelCoords(3424, 560), 10 },
	[16] = { SpawnPixelCoords(3424, 640), 21 },
	[17] = { SpawnPixelCoords(3440, 1008), 3 },
	[18] = { SpawnPixelCoords(3440, 1088), 16 },
	[19] = { SpawnPixelCoords(3472, 768), 12 },
	[20] = { SpawnPixelCoords(3472, 1056), 16 },
	[21] = { SpawnPixelCoords(3472, 1088), 16 },
	[22] = { SpawnPixelCoords(3504, 448), 12 },
	[23] = { SpawnPixelCoords(3504, 1088), 16 },
	[24] = { SpawnPixelCoords(3520, 1008), 19 },
	[25] = { SpawnPixelCoords(3536, 1024), 16 },
	[26] = { SpawnPixelCoords(3536, 1088), 16 },
	[27] = { SpawnPixelCoords(3552, 800), 22 },
	[28] = { SpawnPixelCoords(3584, 288), 5 },
	[29] = { SpawnPixelCoords(3584, 1408), 16 },
	[30] = { SpawnPixelCoords(3600, 1136), 14 },
	[31] = { SpawnPixelCoords(3616, 1328), 18 },
	[32] = { SpawnPixelCoords(3616, 1408), 16 },
	[33] = { SpawnPixelCoords(3712, 1168), 14 },
	[34] = { SpawnPixelCoords(3712, 1376), 12 },
	[35] = { SpawnPixelCoords(3744, 928), 23 },
	[36] = { SpawnPixelCoords(3776, 1328), 16 },
	[37] = { SpawnPixelCoords(3792, 912), 14 },
	[38] = { SpawnPixelCoords(3808, 1168), 16 },
	[39] = { SpawnPixelCoords(3808, 1328), 16 },
	[40] = { SpawnPixelCoords(3808, 1360), 16 },
	[41] = { SpawnPixelCoords(3824, 288), 6 },
	[42] = { SpawnPixelCoords(3840, 1168), 16 },
	[43] = { SpawnPixelCoords(3840, 1328), 16 },
	[44] = { SpawnPixelCoords(3840, 1360), 16 },
	[45] = { SpawnPixelCoords(3856, 1088), 23 },
	[46] = { SpawnPixelCoords(3872, 1168), 16 },
	[47] = { SpawnPixelCoords(3888, 880), 13 },
	[48] = { SpawnPixelCoords(3936, 160), 15 },
	[49] = { SpawnPixelCoords(3936, 1248), 10 },
	[50] = { SpawnPixelCoords(3936, 1376), 10 },
	[51] = { SpawnPixelCoords(3952, 1024), 11 },
	[52] = { SpawnPixelCoords(3968, 160), 15 },
	[53] = { SpawnPixelCoords(4000, 160), 15 },
	[54] = { SpawnPixelCoords(4000, 848), 20 },
	[55] = { SpawnPixelCoords(4000, 1248), 16 },
	[56] = { SpawnPixelCoords(4016, 1168), 2 },
	[57] = { SpawnPixelCoords(4032, 160), 15 },
	[58] = { SpawnPixelCoords(4064, 160), 15 },
	[59] = { SpawnPixelCoords(4064, 176), 15 },
	[60] = { SpawnPixelCoords(4064, 192), 15 },
	[61] = { SpawnPixelCoords(4064, 208), 15 },
	[62] = { SpawnPixelCoords(4064, 224), 15 },
	[63] = { SpawnPixelCoords(4064, 240), 15 },
	[64] = { SpawnPixelCoords(4064, 256), 15 },
	[65] = { SpawnPixelCoords(4064, 272), 15 },
	[66] = { SpawnPixelCoords(4064, 288), 15 },
	[67] = { 0x7FFFFFFF, 0x7FFF, 0 },
};
// clang-format on
