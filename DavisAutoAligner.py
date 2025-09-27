# Davis Auto Aligner
# Developed by Evan Yang
# Documentation by Khalid Yasseen
#
# Set-Up
#
# Required packages: cutadapt, fastqc, trim_galore, bbmap, STAR, multiqc
# Download Genome of interest

import os
outputDir="" #point to your output directory
for fastq in os.scandir(): #scanning through every fastq in the current directory
    #if fastq are unzipped, edit these to .endswith("fastq") & can remove the --readFilesCommand zcat option in CommandAlign
    if fastq.path.endswith(".fastq.gz") and "R2" in fastq.path:
        pass
    if fastq.path.endswith(".fastq.gz") and "R1" in fastq.path: #looking for the forward read file
        currentFile= fastq.path #this is R1
        pairedFile=currentFile.replace("R1","R2") #now we grab its reverse-complement R2
        prefix=currentFile[currentFile.find("/")+1:currentFile.rfind(".")] #create a file name unique to this sample
        fileDir=outputDir+ "/" +str(prefix) #generate a output folder for this sample
        os.mkdir(fileDir) 
        print(fileDir)
        fileQC=fileDir+ "/QC" #generate a folder for QC outputs
        os.mkdir(fileQC)
        commandQC = "fastqc -o "+fileQC+ " "+str(currentFile) #initial QC of R1
        os.system(commandQC)
        print(commandQC)
        commandQC2 = "fastqc -o "+fileQC+ " "+str(pairedFile) #initial QC of R2
        os.system(commandQC2)
        print(commandQC2)
        # # bbmap filtering
        # comment this out if no contamination filtering is required
        # If no filtering: must change clean1 and clean2 in commandTrim to currentFile and pairedFile
        # ensure ref= points to your contamination files, as seen in this command string
        commandbbduk = "bbduk.sh in1="+str(currentFile)+" in2="+str(pairedFile)+" out1=clean1.fastq.gz out2=clean2.fastq.gz ref='/home/ref/humanrRNA.fa.gz','/home/ref/polyT.fa.gz','/home/ref/rRNA.fa','/home/ref/sheep_satellite.fa'"
        clean1 = "clean1.fastq.gz"
        clean2 = "clean2.fastq.gz"
        os.system(commandbbduk)
        print(commandbbduk)
        #running trim galore
        # check options are accurate, specify --cores if needed
        commandTrim="trim_galore --paired --quality 20 --illumina --fastqc --length 15 "+ str(currentFile)+ " "+str(pairedFile)
        #18 is minimum quality for miRNA
        os.system(commandTrim) 
        #aligning via STAR
        for search in os.scandir():
            if "val_1" in search.name and ".fq" in search.name: #finding trimmed R1 sample
                val1= search.name
            if "val_2" in search.name and ".fq" in search.name: #finding trimmed R2 sample
                val2= search.name
        # STAR Aligner
        # CHECK OPTIONS ARE ACCURATE - biggest source of script erroring out
        # Consider defining --runThreadN to your available cores
        # Refer to the STAR manual for more options
        # This is the command at its most basic form
        commandAlign="STAR --genomeDir /home/Genome --readFilesIn "+str(val1)+" "+str(val2)+" --readFilesCommand zcat --quantMode GeneCounts --genomeLoad LoadAndKeep --outFileNamePrefix " +str(prefix) 
        print(commandAlign)
        os.system(commandAlign)
        #moves all remaining output files to output directory
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
    #Post alignment QC
    commandmultiQC = "multiqc "+fileDir+" -o "+fileQC
    os.system(commandmultiQC)

# This aligner can be modified to serve a number of use cases: 
# - miRNA alignment using mirDeep2
# - multi genome alignments
# - additional sample pre-processing
# - single end read alignment

