class BioPepaCsvParser():
    def openCsv(self,csv):
        with open(csv, 'r') as f:
            results_dict = {}
            
            contents = f.readlines()
            
            keys = contents[7].split(',')
            
            keys[0] = keys[0][2:]
            results_dict[keys[0]] = []
            
            for i in range(1,len(keys)):
                keys[i] = keys[i].strip()[1:-1]
                results_dict[keys[i]] = []
            
            print results_dict.keys()
            
            data = contents[8:]
            
            for row in data:
                row = row.split(',')
                for i in range(0,len(row)):
                    results_dict[keys[i]] += [row[i].strip()]
                    
            print results_dict['Time']
            print results_dict['R']
            print results_dict['aSrc_total_MB']
            
x = BioPepaCsvParser()
x.openCsv('r_asrc.csv')
