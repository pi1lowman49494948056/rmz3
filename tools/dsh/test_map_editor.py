"""Regression tests: every mutation happens in a temporary project copy."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('editor', Path(__file__).with_name('map_editor.py'))
editor = importlib.util.module_from_spec(spec); spec.loader.exec_module(editor)

class RoomTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        for f in ['tools/dsh/room.json','tools/dsh/map.txt','tools/dsh/baseline/landscape.c.txt','tools/dsh/baseline/screen.bin',editor.LC,editor.SCRIPT]:
            q=self.root/f;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(editor.ROOT/f,q)
    def config(self, edit):
        p=self.root/'tools/dsh/room.json';c=json.loads(p.read_text());edit(c);p.write_text(json.dumps(c))
    def test_current_and_idempotence(self):
        outputs,_=editor.generate(self.root)
        for p,b in outputs.items():p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        again,_=editor.generate(self.root);self.assertEqual(outputs,again)
    def test_shrink_removes_old_region(self):
        p=self.root/'tools/dsh/map.txt';rows=p.read_text().splitlines();p.write_text('\n'.join(r[:238]+'##' for r in rows)+'\n')
        self.config(lambda c:c['teleport'].update(trigger_left_px=3500))
        outputs,_=editor.generate(self.root);s=outputs[self.root/editor.LC].decode()
        grid=editor.array(s,'sChunkMap1')[2];behavior=editor.array(s,'sScreenBehavior')[2]
        self.assertEqual(grid[10*32+19],1);self.assertEqual(behavior[10*32+19]>>12,15)
        self.assertEqual(behavior[10*32+15]>>12,0)
    def test_widen_and_move_origin(self):
        p=self.root/'tools/dsh/map.txt';rows=p.read_text().splitlines()
        rows=[r[:-2]+('###############' if y>=18 else '...............')+'##' for y,r in enumerate(rows)]
        p.write_text('\n'.join(rows)+'\n');self.config(lambda c:c.update(origin_chunk=[1,8]))
        outputs,_=editor.generate(self.root);hdr=outputs[self.root/'include/dsh_room_config.h'].decode()
        self.assertIn('#define DSH_TARGET_X 640',hdr);self.assertIn('#define DSH_TARGET_Y 1568',hdr)
    def test_invalid_spawn_no_writes(self):
        self.config(lambda c:c.update(spawn_px=[1312,272]))
        before=(self.root/editor.LC).read_bytes()
        with self.assertRaisesRegex(ValueError,'no solid floor'):editor.generate(self.root)
        self.assertEqual(before,(self.root/editor.LC).read_bytes())
    def test_missing_wall(self):
        p=self.root/'tools/dsh/map.txt';p.write_text('.'+p.read_text()[1:])
        with self.assertRaisesRegex(ValueError,'walls'):editor.generate(self.root)
    def test_overflow(self):
        self.config(lambda c:c.update(origin_chunk=[20,9]))
        with self.assertRaisesRegex(ValueError,'exceeds'):editor.generate(self.root)
    def test_decorative_chunks_preserved(self):
        outputs,_=editor.generate(self.root);old=(self.root/'tools/dsh/baseline/screen.bin').read_bytes();new=outputs[self.root/editor.BIN]
        source=(self.root/'tools/dsh/baseline/landscape.c.txt').read_text(encoding='utf8')
        for name in ['sChunkMap2','sChunkMap3']:
            for cid in set(editor.array(source,name)[2]):self.assertEqual(old[cid*300:(cid+1)*300],new[cid*300:(cid+1)*300])

if __name__=='__main__':unittest.main()
