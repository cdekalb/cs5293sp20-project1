import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, 
        help="Text file on which redactions will be implemented.")
    parser.add_argument("--input", type=str, required=False,
        help="Other files to on which redactions will be implemented")
# TODO: Figure out alternate parsers. Writing method for a flag?
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)