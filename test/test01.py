import pandas as pd
from tqdm import tqdm

from config import ChainEnum
from digger.parser import Parser

if __name__ == '__main__':

    for bridge in ["Celer", "Multi", "Poly"]:
        print(f"------ Current Bridge: {bridge} ------")
        df = pd.read_csv(f"../data/FirstPhrase/{bridge}_ETH.csv")

        success = 0
        for hash in tqdm([e['hash'] for e in df.to_dict("records")]):
            try:
                parser = Parser(ChainEnum.BNB)
                elogs = parser.get_event_logs(hash)
                success += 1
                print(elogs)
                exit(0)
            except Exception as e:
                pass

        print(f"------ Current Bridge: {bridge}, Success: {success} ------")





