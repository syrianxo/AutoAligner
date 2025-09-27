#!/home/kyasseen/miniconda3/envs/daviscompnerds/bin/python
#-*- coding: utf-8 -*-
import os
import pdb
outputDir="/home/kyasseen/Fontan_total/Output"
#os.mkdir(outputDir)
for fastq in os.scandir():
    if fastq.path.endswith(".fastq.gz") and "R2" in fastq.path:
        pass
    if fastq.path.endswith(".fastq.gz") and "R1" in fastq.path:
        currentFile= fastq.path
        pairedFile=currentFile.replace("R1","R2")
        prefix=currentFile[currentFile.find("/")+1:currentFile.rfind(".")]
        fileDir=outputDir+ "/" +str(prefix)
        os.mkdir(fileDir) 
        print(fileDir)
        fileQC=fileDir+ "/QC"
        os.mkdir(fileQC)
        commandQC = "fastqc -o "+fileQC+ " "+str(currentFile)
        os.system(commandQC)
        print(commandQC)
        commandQC2 = "fastqc -o "+fileQC+ " "+str(pairedFile)
        os.system(commandQC2)
        print(commandQC2)
        # bbmap filtering
        commandbbduk = "bbduk.sh in1="+str(currentFile)+" in2="+str(pairedFile)+" out1=clean1.fastq.gz out2=clean2.fastq.gz ref=/home/kyasseen/ref/humanrRNA.fa.gz"
        clean1 = "clean1.fastq.gz"
        clean2 = "clean2.fastq.gz"
        os.system(commandbbduk)
        print(commandbbduk)
        #running trim galore
        commandTrim="trim_galore --paired --cores 2 --quality 20 --illumina --fastqc --length 15 "+ str(clean1)+ " "+str(clean2)
        #18 is minimum for miRNA? idk pick setting
        os.system(commandTrim) 
        #aligning via star
        for search in os.scandir():
            if "val_1" in search.name and ".fq" in search.name:
                val1= search.name
            if "val_2" in search.name and ".fq" in search.name:
                val2= search.name
        commandAlign="STAR --runThreadN 12 --genomeDir /home/kyasseen/Genome --readFilesIn "+str(val1)+" "+str(val2)+" --readFilesCommand zcat --quantMode GeneCounts --outFilterScoreMinOverLread 0.33 --outFilterMatchNminOverLread 0.33 --outFilterMatchNmin 0.33 --outFilterMismatchNmax 2 --outReadsUnmapped Fastx --outSAMtype BAM Unsorted --genomeLoad LoadAndKeep --outFileNamePrefix " +str(prefix) 
        print(commandAlign)
        os.system(commandAlign)
        #moves all random files
        for file in os.scandir():
            print(file.path)
            if file.path.endswith(".txt"):
                fileName=file.path[file.path.rfind("/")+1:]
                newDir=fileDir+"/"+fileName
                os.rename(file.path, newDir)
            if file.path.endswith(".out"):
                fileName=file.path[file.path.rfind("/")+1:]
                newDir=fileDir+"/"+fileName
                os.rename(file.path, newDir)
            if file.path.endswith(".bam"):
                fileName=file.path[file.path.rfind("/")+1:]
                newDir=fileDir+"/"+fileName
                os.rename(file.path, newDir)
            if file.path.endswith(".zip"):
                fileName=file.path[file.path.rfind("/")+1:]
                newDir=fileDir+"/"+fileName
                os.rename(file.path, newDir)
            if file.path.endswith(".fq.gz"):
                fileName=file.path[file.path.rfind("/")+1:]
                newDir=fileDir+"/"+fileName
                os.rename(file.path, newDir)
            if file.path.endswith(".html"):
                fileName=file.path[file.path.rfind("/")+1:]
                newDir=fileDir+"/"+fileName
                os.rename(file.path, newDir)
            if file.path.endswith(".tab"):
                fileName=file.path[file.path.rfind("/")+1:]
                newDir=fileDir+"/"+fileName
                os.rename(file.path, newDir)
            if file.path.endswith("clean1.fastq.gz"):
                fileName=file.path[file.path.rfind("/")+1:]
                newDir=fileDir+"/"+fileName
                os.rename(file.path, newDir)
            if file.path.endswith("clean2.fastq.gz"):
                fileName=file.path[file.path.rfind("/")+1:]
                newDir=fileDir+"/"+fileName
                os.rename(file.path, newDir)
            if file.path.endswith(".mate1"):
                fileName=file.path[file.path.rfind("/")+1:]
                newDir=fileDir+"/"+fileName
                os.rename(file.path, newDir)
            if file.path.endswith(".mate2"):
                fileName=file.path[file.path.rfind("/")+1:]
                newDir=fileDir+"/"+fileName
                os.rename(file.path, newDir)
        #final QC
    commandmultiQC = "multiqc "+fileDir+" -o "+fileQC
    os.system(commandmultiQC)


def qual_check(file, qc):
    if(qc == fastqc):
        commandQC = "fastqc" +file
        os.system(commandQC)
        for file in os.scandir()


# bbduk.sh -> bbmap, conda
# create a reference fasta

# multiqc (conda)

# BLAST any overrepresented sequences or unmapped

# de novo assembly

# --sjdbGTFfiles inputted in the alignment step

# --sjdbOverhang 99, sketq -> readlengths, var = sketq <- readlengths - 1 , --sjdbOverhang var

# transcriptome, kallisto -> aligns to transcript, but we need an annotated transcript file for sheep

# sequencing file format, all the reads are inputted ... sketq readlengths then collect all the log.final.out inputted read lengths === 


STAR --runThreadsN 12 --genomeDir /home/kyasseen/Sheep_Genome --readFilesIn p21153-s001_1-EV_TotalRNA_S1_L002_R1_001.fastqUnmapped.out.mate1 --quantMode GeneCounts --outReadsUnmapped Fastx --outFileNamePrefix p21153-s001_1-EV_TotalRNA_S1_L002_R1_001_UnmappedAlign --outSAMtype BAM Unsorted

STAR --runThreadsN 12 --genomeDir /home/kyasseen/Sheep_Genome --readFilesIn p21153-s001_1-EV_TotalRNA_S1_L002_R1_001.fastqUnmapped.out.mate1 --quantMode GeneCounts --outReadsUnmapped Fastx --outFileNamePrefix p21153-s001_1-EV_TotalRNA_S1_L002_R1_001_UnmappedAlign --outSAMtype BAM Unsorted --sjdbOverhang 98 --outFileNamePrefix