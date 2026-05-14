import numpy as np
import urenderer

    # Crie uma cena com três objetos, um filho do outro:
    # Objeto0 -> Objeto1 -> Objeto2
    #
    # Configure as transformações para que todos os objetos sejam visíveis e renderize a cena
    #
    # Altere a transformação do objeto avô dos outros e renderize a cena.
    # Observe como que os objetos filhos se movem juntos

if __name__ == "__main__":
        urenderer.utils.clear_workdir("03-grandchild")
        renderer = urenderer.renderer.PyplotRenderer(1920, 1080)
        runtime = urenderer.application.Runtime(renderer, name="03-grandchild")

        # Crie a cena
        piramide_obj0 = urenderer.node.Node()

        piramide_obj0.render_data = urenderer.geometry.polygonal_ifs.get_ifs_pyramid()
        
        piramide_obj1 = urenderer.node.Node()

        piramide_obj1.render_data = urenderer.geometry.polygonal_ifs.get_ifs_pyramid()
        
        piramide_obj1.translation = np.array([0, 0.5, 0], np.float64)

        piramide_obj0.add_child(piramide_obj1)

        cubo_obj2 = urenderer.node.Node()

        cubo_obj2.render_data = urenderer.geometry.polygonal_ifs.get_ifs_cube()
        cubo_obj2.translation = np.array([0.5, 0, 0], np.float64)

        piramide_obj1.add_child(cubo_obj2)

        runtime.scene.add_child(piramide_obj0)

        runtime.iter(capture=True)

        # Rotacione o nó avô
        piramide_obj0.rotation = np.array([45, 45, 45], np.float64)

        runtime.iter(capture=True)
