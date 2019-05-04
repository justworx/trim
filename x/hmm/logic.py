#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


TERMS = [
	'MAJOR',  # Major Premise
	'MINOR',  # Minor Premise
	'THESIS'  # Conclusion
]

#
# RULES:
#  - The MAJOR and MINOR premises must have one term in common with
#    the THESIS.
#  - The term that is in both the MAJOR premise and the THESIS 
#    is the major term - it's the Predicate of the THESIS and must
#    state something about the Subject of the THESIS.
#  - The term shared by the minor premise and the THESIS is the 
#    MINOR term. It's the subject of the THESIS.
#





#
# FIGURE
#  - A syllogism’s figure is determined by whether the middle term 
#    serves as subject or predicate in the premises. Recall that a 
#    subject is what the sentence is about, and the predicate is a 
#    word that applies to the subject of the sentence.
#

#
# In a first figure syllogism, the middle term serves as subject in 
# the major premise and predicate in the minor premise: "All birds 
# are animals. All parrots are birds. All parrots are animals".
# 


VALID_FORMS = [
	['AAA', 'EAE', 'AII', 'EIO'],               # FIRST_FIGURE
	['EAE', 'AEE', 'EIO', 'AOO'],               # SECOND_FIGURE
	['AAI', 'IAI', 'AII', 'EAO', 'OAO', 'EIO'], # THIRD_FIGURE
	['AAI', 'AEE', 'IAI', 'EAO', 'EIO']         # FOURTH_FIGURE
]
