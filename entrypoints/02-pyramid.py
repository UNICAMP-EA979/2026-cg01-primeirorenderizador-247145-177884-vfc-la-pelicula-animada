import numpy as np
import urenderer

# Crie uma cena contendo uma pirâmide e renderize ela
#
# Implemente urenderer.geometry.polygonal_ifs.get_ifs_pyramid para obter a geometria de uma pirâmide

if __name__ == "__main__":
    urenderer.utils.clear_workdir("02-pyramid")
    renderer = urenderer.renderer.PyplotRenderer(1920, 1080)
    runtime = urenderer.application.Runtime(renderer, name="02-pyramid")

    piramide = urenderer.node.Node()

    piramide.render_data = urenderer.geometry.polygonal_ifs.get_ifs_pyramid()

    runtime.scene.add_child(piramide)

    runtime.iter(capture=True)
