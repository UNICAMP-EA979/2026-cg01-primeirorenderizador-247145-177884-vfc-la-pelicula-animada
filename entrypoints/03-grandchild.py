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
    

    runtime.iter(capture=True)

    # Rotacione o nó avô
    transform = piramide_obj0.get_component(urenderer.component.TransformComponent)
    transform.rotation[1] = 45.0 # Rotacione 45 graus no eixo Y

    runtime.iter(capture=True)
