import os
from pandas import read_csv
import csv

class properties:
    def __init__(self, date, electrode, solute, concentration, technique):
        self.date = date
        self.electrode = electrode
        self.solute = solute
        self.concentration = concentration
        self.technique = technique

def dat2csv(basedir):
    dpvdir = "{}\data.csv".format(basedir)
    cvdir = "{}\dataCV.csv".format(basedir)

    BGE = {"directory": "{}\BGE".format(basedir), "electrode": "Bare Gold"}
    S2 = {"directory": "{}\S2".format(basedir), "electrode": "S2"}
    S3 = {"directory": "{}\S3".format(basedir), "electrode": "S3"}

    w = open(dpvdir, 'w+', newline='')  # DPV/SWV data csv
    c = open(cvdir, 'w+', newline='')   # CV data csv

    datwriter = csv.writer(w, delimiter=',')
    cvwriter = csv.writer(c, delimiter=',')

    datwriter.writerow(["date", "electrode", "solute", "concentration", "technique", "estep", "idelta"])
    cvwriter.writerow(["date", "electrode", "solute", "concentration", "technique", "cycle", "ewe", "i"])

    writers = {"DPV": datwriter, "CV": cvwriter}

    for filepath in [BGE, S2, S3]:
        for file in os.listdir(filepath["directory"]):
            metadata = metadataparse(file, filepath["electrode"])
            dataparse(metadata, r'{}\{}'.format(filepath["directory"], file), writers)


def dataparse(metadata, datafile, writers):
    data = read_csv(datafile, delimiter="\t")

    if metadata.technique == "CV":
        ewe = data.iloc[:, 0]
        i = data.iloc[:, 1]
        cycle = data.iloc[:, 2]

        for j in range(len(cycle)):
            writers["CV"].writerow(
                [
                    metadata.date,
                    metadata.electrode,
                    metadata.solute,
                    metadata.concentration,
                    metadata.technique,
                    int(cycle[j]),
                    ewe[j],
                    i[j]
                 ]
            )

    elif metadata.technique == 'DPV' or metadata.technique == 'SWV':
        estep = data.iloc[:, 0]
        idelta = data.iloc[:, 1]

        for j in range(len(estep)):
            if idelta[j] == 0:
                continue
            writers["DPV"].writerow(
                [
                    metadata.date,
                    metadata.electrode,
                    metadata.solute,
                    metadata.concentration,
                    metadata.technique,
                    estep[j],
                    idelta[j]
                ]
            )
    else:
        raise Exception("Test technique could not be ascertained: Line 55\nCheck filename:\t{}".format(datafile))
    return 1


def metadataparse(filename, electrode):
    concentration = solute = date = technique = None

    for t in ['DPV', 'SWV', 'CV']:
        if t in filename:
            technique = t
            break

    if 'Salt' in filename:
        concentration = 0
        solute = 'Salt'

    else:
        for s in ['[1to1]', '[2to1]', '[1to2]', 'Lactate', 'Succinate']:
            if s in filename:
                solute = s
                break

        # Need to replace this with regex in the future
        for c in ['_0.1mM', '_0.1uM', '_1mM', '_1uM', '_10mM', '_10uM', '_100mM']:
            if c in filename:
                concentration = c[1:]
                break

    date = filename[4:6]+"-"+filename[6:8]+"-"+filename[0:4]
    metadata = properties(date, electrode, solute, concentration, technique)

    try:
        solute + str(concentration) + technique + date

    except:
        print("Metadata could not be determined from filename!\n"
              "Check the following filename for errors: {}".format(filename))

    return metadata


def main():
    basedir = r"C:\Users\DominicLannutti\Desktop\Trial 3&4 Combined"
    dat2csv(basedir)


if __name__ == "__main__":
    main()