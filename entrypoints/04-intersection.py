import numpy as np
import urenderer

# Renderize uma cena em que o algoritmo de oclusão falha
#
# Observe o método urenderer.renderer.pyplot_renderer.PyplotRenderer::end
# Ele desenha a cena utilizando o "algoritmo do pintor" (painter's algorithm)
# para determinar a visibilidade dos triângulos (qual deve estar por cima do outro)
#
# Crie uma cena com dois cubos de forma que o algoritmo do pintor falhe de forma
# visualmente perceptível.

if __name__ == "__main__":
    urenderer.utils.clear_workdir("04-intersection")
    renderer = urenderer.renderer.PyplotRenderer(1920, 1080)
    runtime = urenderer.application.Runtime(renderer, name="04-intersection")

    # Crie a cena

    cubo_obj1 = urenderer.node.Node()
    cubo_obj2 = urenderer.node.Node()

    cubo_obj1.render_data = urenderer.geometry.polygonal_ifs.get_ifs_cube()
    cubo_obj1.translation = np.array([0.5, 0.25, 0.25], np.float64)
    cubo_obj2.render_data = urenderer.geometry.polygonal_ifs.get_ifs_cube()
    cubo_obj2.translation = np.array([0.5, 0, 0], np.float64)

    runtime.scene.add_child(cubo_obj1)
    runtime.scene.add_child(cubo_obj2)

    runtime.iter(capture=True)