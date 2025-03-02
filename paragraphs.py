def main():
    with open('paragraphs.txt', 'r') as file:
        input = file.readlines()
    paragraphs = []
    for i in input:
        paragraphs.append(i.strip('\n'))
    print(paragraphs)


if __name__ == "__main__":
    main()