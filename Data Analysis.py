import pickle


def main():
    out_file = open('output.data', 'rb')
    data = pickle.load(out_file)
    out_file.close()

    for item in data:
        print(item)  # TODO Analzye Data


if __name__ == "__main__":
    main()
