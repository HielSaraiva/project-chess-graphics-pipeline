def save_ppm(framebuffer, filename, width, height):
    """
    Exporta a matriz do framebuffer para o formato de arquivo de imagem PPM.
    """
    with open(filename, "w") as file:

        file.write(f"P3\n{width} {height}\n255\n")

        for row in framebuffer:

            for pixel in row:

                r, g, b = pixel

                file.write(
                    f"{r} {g} {b} "
                )

            file.write("\n")