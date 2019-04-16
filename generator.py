import os
import cairosvg


def generate_single_sdf(sdf_path, out_sdf_dir):
    print("reading from", sdf_path, "...")

    single_sdf_s = [""]
    with open(sdf_path, "r") as sdf:
        for line in sdf.readlines():
            single_sdf_s[-1] += line
            if line == "$$$$\n":
                single_sdf_s.append("")

    print("generating to", out_sdf_dir, "...")
    for single_sdf in single_sdf_s:
        if single_sdf != "":
            with open(os.path.join(out_sdf_dir, single_sdf.splitlines()[0].strip()), "w") as generated_sdf:
                generated_sdf.write(single_sdf)


def generate_q_and_a(single_sdf_dir, out_svg_dir, out_answer_dir):
    for name in os.listdir(single_sdf_dir):
        path = os.path.join(single_sdf_dir, name)
        answer = ""
        with open(path, "r") as single_sdf:
            for line in single_sdf.readlines():
                if line.startswith(" " * 4):
                    answer += line.split()[3]

        out_answer_path = os.path.join(out_answer_dir, name)
        with open(out_answer_path, "w") as answer_file:
            answer_file.write(answer)

        out_svg_path = os.path.join(out_svg_dir, name)
        os.system("tool\\mol2svg.exe {} >{}".format(path, out_svg_path))


def generate_png(svg_dir, out_png_dir):
    for name in os.listdir(svg_dir):
        path = os.path.join(svg_dir, name)
        out_path = os.path.join(out_png_dir, name)

        with open(path, "r") as svg:
            cairosvg.svg2png(bytestring=svg.read(), write_to=out_path)


if __name__ == '__main__':

    generate_single_sdf("data/SDF/Compound_000000001_000025000.sdf",
                        "data/generated/question/SDF")
    generate_q_and_a("data/generated/question/SDF",
                     "data/generated/question/SVG",
                     "data/generated/answer")
    generate_png("data/generated/question/SVG",
                 "data/generated/question/PNG")

