# Basic motion detection and tracking with Python and OpenCV
[Site](https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
)  
### Funcionamento

O Primeiro Frame da captura será a Referência(background).

### Desvantens

1. Mexeu um pouco a posição da câmera, o código já muda o estado como ocupado.

2. Mudança de iluminação também mudam o estado para ocupado.

### Possível Solução

1. Ficar atualizando a imagem de Referência

![img](https://www.pyimagesearch.com/wp-content/uploads/2015/05/animated_motion_02.gif)
