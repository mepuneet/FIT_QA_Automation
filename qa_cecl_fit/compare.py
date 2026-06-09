from const import ALL_FILES,CommonPaths,BANK_ID
import glob
import os

def compare_fitqa_newqa(fit_file,qa_file,bank_no,file_name):
	try:
		with open(fit_file, 'r') as ff, open(qa_file, 'r') as qf:
			error_counts = 0
			for i,(ff_line, qf_line) in enumerate(zip(ff, qf)):
				ff_line = ff_line.strip()
				qf_line = qf_line.strip()

				if ff_line != qf_line:
					ff_cells = ff_line.split("\t")
					qf_cells = qf_line.split("\t")

					#in total Fit "has space"
					if len(ff_cells)-1 == len(qf_cells):
						if "\t \t" in ff_line:
							ff_line = ff_line.replace("\t \t","\t")
						elif "\t\xa0\t" in ff_line:
							ff_line = ff_line.replace("\t\xa0\t","\t")
						elif "\t\t" in ff_line:
							ff_line = ff_line.replace("\t\t","\t")

						ff_cells = ff_line.split("\t")

					for col_i,(ff_cell,qf_cell) in enumerate(zip(ff_cells,qf_cells)):

						# for first two rows
						# header are shifted ..
						# length is different 
						# starting may diff but end must same
						if i <2 and  col_i ==0 and len(ff_cells) !=len(qf_cells) and ff_cell.strip() != qf_cell.strip():#  and (ff_cells[-1].strip() == qf_cells[-1].strip()):
							print(f"..........HEADERS SHIFTED .. {bank_no} row:{i},col:{col_i}: {file_name}:  {ff_cell} != {qf_cell}")
							break
						elif ff_cell.strip() != qf_cell.strip():
							print(f"DATA MISMATCH .. {bank_no} row:{i},col:{col_i}: {file_name}:  {ff_cell} != {qf_cell}")
							error_counts +=1
			
			if error_counts:
				print("-"*50)
				breakpoint()
		print("compared ---",fit_file)
	except Exception as e:
		print(e)
	# print("-"*100,fit_file)

def compare_by_bank(bank_id):
	before_after=1
	fit_path = CommonPaths.get_fit_path(bank_id)
	skq_path = CommonPaths.get_skq_path(bank_id)
	for file_config in ALL_FILES:
		file_ = file_config.get('file_name')
		fit_file = f"{fit_path}{file_}"
		qa_file = f"{skq_path}{file_}"

		if not os.path.isfile(fit_file):
			# print("File not found",fit_file)
			continue

		if not os.path.isfile(qa_file):
			fit_size = os.path.getsize(fit_file)
			if fit_size>0:
				print("File not found-- ",qa_file)
			continue

		compare_fitqa_newqa(fit_file,qa_file,bank_id,file_)

# def check_exist_files(fit_file,qa_file):
# 	if os.path.isfile(fit_file) and os.path.getsize(fit_file) ==0:
# 		return False
	
# 	if not os.path.isfile(qa_file):
# 		fit_size = os.path.getsize(fit_file)
# 		if fit_size>0:
# 			print("File not found-- ",qa_file)

# 	if not os.path.isfile(fit_file):
# 		qa_size = os.path.getsize(qa_file)
# 		if qa_size>0:
# 			print("File not found-- ",qa_file)


if __name__ == "__main__":
	bank_id = input("Bank No: ")
	bank_id = BANK_ID if len(bank_id) < 3 else bank_id
	compare_by_bank(bank_id)