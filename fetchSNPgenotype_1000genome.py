### modified scripts from somewhere
### download genotype data for human 1000 genome project from ENSEMBL browser by rsID
## 

import requests, sys
import pandas as pd

def get_genotype_ensembl(snp):
    server = "http://rest.ensembl.org"
    ext = "/variation/human/" + snp + "?genotypes=1"
     
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
     
    if not r.ok:
      r.raise_for_status()
      sys.exit()
     
    decoded = r.json()
    print str(len(decoded['genotypes'])) + " samples are retrieved from ENSEMBL for SNP " + snp
    
    dfin = []
    for i in range(len(decoded['genotypes'])):
        sex = decoded['genotypes'][i]['gender']
        sample = decoded['genotypes'][i]['sample'].replace("1000GENOMES:phase_3:","")
        geno = decoded['genotypes'][i]['genotype'].replace("|","")
        dfin.append([sample, sex, geno])

    dfin = pd.DataFrame(dfin, columns=['sample','sex', snp])  
    
    return dfin

## define a snp list
snps = ["rs7566597","rs9883818","rs150230900","rs953897"]

## fetch genotype for each SNP
dout = []
for i in snps:
    dout.append(get_genotype_ensembl(i))

## merge genotype
df_final = reduce(lambda left,right: pd.merge(left,right,on='sample', how="inner"), dout)
df_final.sort_values(['sample']).to_csv("Test.csv", index=False)