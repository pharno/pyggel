import pyggel
from pyggel import *

import random

def main():
    pyggel.view.init(screen_size=(800,600), screen_size_2d=(640, 480))
    pyggel.view.set_debug(False)

    my_light = pyggel.light.Light((0,100,0), (0.5,0.5,0.5,1),
                                  (1,1,1,1), (50,50,50,10),
                                  (0,0,0), True)

    camera = pyggel.camera.LookAtCamera((0,0,0), distance=10)

    img = pyggel.image.Image("data/tile_example.png", pos=(50, 50))
    img.colorize=(1,0,0,1)
    img2 = pyggel.image.Image("data/ar.png", pos=(50,0))
    img2.colorize=(1,1,1,0.5)
    img3d = []
    for x in xrange(10):
        img3d.append(pyggel.image.Image3D("data/tile_example.png",
                                          pos=(random.randint(-10, 10),
                                               random.randint(-10, 10),
                                               10)))

    font = pyggel.font.MEFont()
    font3d = pyggel.font.Font(font_char_height3d=0.3)
    img4 = font.make_text_image("Hello World: 2D", (1, 1, 0, 1), underline=True, italic=True, bold=True)
    img4.pos = (50,50)
    img5 = font3d.make_text_image3D("Hello World: 3D", (0, 1, 1, 1))
    img5.scale = 2

    img6 = pyggel.image.GIFImage("data/smiley.gif", pos=(150, 150))
    img7 = pyggel.image.GIFImage3D("data/smiley.gif", pos=(0,0,1))

    pyggel.view.set_cursor(pyggel.image.SpriteSheet("data/ar.png",
                                    [(0,0,16,16), (16,0,16,16), (32,0,16,16), (16,0,16,16)],
                                    100),
                           True)

    obj = pyggel.mesh.OBJ("data/bird_plane.obj")
    obj.scale = .5
    obj2 = obj.copy()
    obj2.pos = (0,0,5)

    box = pyggel.geometry.Cube(5, texture=data.Texture("data/stickdude.png"))
    box.pos = (-5, 0, 0)

    box2 = pyggel.geometry.Cube(5, texture=data.Texture("data/skybox.png"), mirror=False)
    box2.pos = (5, 0, 0)

    verts = [(0,0,0),
             (0,1,0),
             (1,0,0)]
    batch = pyggel.misc.BatchVertObject(verts)

    my_scene = pyggel.scene.Scene()
    my_scene.pick = True
    my_scene.add_2d(img)
    my_scene.add_2d(img2)
    my_scene.add_2d(img4)
    my_scene.add_2d(img6)

    my_scene.add_3d(obj)
    my_scene.add_3d(obj2)
    my_scene.add_3d((box, box2, batch))
    for i in img3d:
        my_scene.add_3d(i)
    my_scene.add_3d(img5)
    my_scene.add_3d(img7)

    my_scene.add_light(my_light)
    my_scene.camera = camera

    clock = pygame.time.Clock()

    rot = 0

    last_hit = None

    meh = pyggel.event.Handler()
    meh.bind_to_event(" ", lambda a,b: pyggel.misc.save_screenshot("Test.png"))

    while 1:
        clock.tick(999)
        pyggel.view.set_title("FPS: %s"%clock.get_fps())

        meh.update()

        if meh.quit:
            pyggel.quit()
            return None
        if "left" in meh.mouse.hit:
            if img.get_rect().collidepoint(pyggel.view.screen.get_mouse_pos2d()):
                print 32
        if "right" in meh.mouse.hit:
            cur = view.screen.cursor
            if cur.running:
                cur.pause()
            else:
                cur.play()

        if K_LEFT in meh.keyboard.active:
            camera.roty -= .5
        if K_RIGHT in meh.keyboard.active:
            camera.roty += .5
        if K_DOWN in meh.keyboard.active:
            camera.rotx -= .5
        if K_UP in meh.keyboard.active:
            camera.rotx += .5
        if K_1 in meh.keyboard.active:
            camera.rotz -= .5
        if "2" in meh.keyboard.active: #just to throw you off ;)
            camera.rotz += .5

        if "=" in meh.keyboard.active:
            camera.distance -= .1
        if "-" in meh.keyboard.active:
            camera.distance += .1

        if "a" in meh.keyboard.active:
            camera.posx -= .1
        if K_d in meh.keyboard.active:
            camera.posx += .1
        if K_s in meh.keyboard.active:
            camera.posz -= .1
        if K_w in meh.keyboard.active:
            camera.posz += .1

        rot += 1
        a,b,c = img.rotation
        c += 1
        img.rotation = a,b,c

        a,b,c = img2.rotation
        c -= 1
        img2.rotation = a,b,c

        img5.visible = not img5.visible

        pyggel.view.clear_screen(my_scene)

        hit = my_scene.render()#camera)
        if last_hit:
            last_hit.outline = False
        if hit:
            hit.outline = True
        last_hit = hit

        mpx, mpy = pyggel.view.screen.get_mouse_pos()

        pyggel.view.refresh_screen()
main()
