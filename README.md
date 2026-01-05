# MCQ-application
This project is a Python based MCQ desktop application that supports various quiz modes, assessment management, review tools, and certification exams. The project also includes whitebox and blackbox test cases.

Uncompress the project zip file: Right click on the ZIP file and select extract all.

Import the project: Open a terminal and navigate to the project directory or open the folder straight away in Pycharm application.

To run the application: On the terminal, enter the following command:
python3 main.py

To run test cases:

Testing commands of 259025897 (Mrudhulaa):
1. Blackbox testing:

python -m unittest \
  testing.259025897.test.blackbox.category_partition.fn_1_take_quiz.test_take_quiz -v

python -m unittest \
  testing.259025897.test.blackbox.category_partition.fn_2_timed_quiz.test_timed_quiz -v
  
  python -m unittest \
  testing.259025897.test.blackbox.category_partition.fn_3_negative_marking_quiz.test_negative_marking_quiz -v 
  
  python -m unittest \
  testing.259025897.test.blackbox.category_partition.fn_4_quiz_challenge.test_quiz_challenge -v
  
  python -m unittest \
  testing.259025897.test.blackbox.category_partition.fn_5_take_quiz_until_wrong.test_take_quiz_until_wrong -v
  
  python -m unittest \
  testing.259025897.test.blackbox.category_partition.fn_6_learning_mode_quiz.test_learning_mode -v

python -m unittest \
  testing.259025897.test.blackbox.category_partition.fn_7_create_assessments.test_create_assessments -v
  
  python -m unittest \
  testing.259025897.test.blackbox.category_partition.fn_8_manage_assessments.test_manage_assessments -v
  
  python -m unittest \
  testing.259025897.test.blackbox.category_partition.fn_9_view_assessments.test_view_assessments -v

2. Whitebox testing:

2.1 Branch testing:

coverage run --branch --source=mcq_types,manage_assessment,assessment_storage -m unittest \
  testing.259025897.test.whitebox.branch_testing.test_branch_mcq_types \
  testing.259025897.test.whitebox.branch_testing.test_branch_assessment \
  testing.259025897.test.whitebox.branch_testing.test_branch_assessment_storage

Command for Branch testing coverage: 

coverage report -m

2.2 Statement testing:

coverage run --source=mcq_types,manage_assessment,assessment_storage \
-m unittest testing/259025897/test/whitebox/statement_testing/statement_test.py

Command for statement testing coverage:

coverage report -m

2.3 Loop testing:

python3 -m unittest testing/259025897/test/whitebox/loop_testing/loop_test.py

2.4 Condition testing:

python3 -m unittest testing/259025897/test/whitebox/condition_testing/condition_test.py

2.5 Concolic testing:

coverage run --source=mcq_types,manage_assessment,assessment_storage \
-m unittest testing/259025897/test/whitebox/concolic_testing/concolic_test.py

Command for concolic testing coverage:

coverage report -m

-----------------------------------------------------------------------------------------------------------------
Testing commands of 259044798 (Devyani):

1. Blackbox testing:

python -m unittest testing.259044798.test.blackbox.category_partition.fn_1_comparison_quiz_attempts.test_comparison_quiz_attempts

python -m unittest testing/259044798/test/blackbox/category_partition/fn_2_take_quiz_with_skip/test_take_quiz_with_skip.py

python -m unittest testing.259044798.test.blackbox.category_partition.fn_3_show_all_answers.test_show_all_answers

python -m unittest discover testing/259044798/test/blackbox/category_partition/fn_4_age_based_quiz

python -m unittest testing.259044798.test.blackbox.category_partition.fn_5_answers_link.test_answers_link

python -m unittest testing/259044798/test/blackbox/category_partition/fn_6_quiz_attempts/test_quiz_attempts.py

python -m unittest testing/259044798/test/blackbox/category_partition/fn_7_fill_in_the_blanks/test_fill_in_the_blanks.py

2. Whitebox testing:

2.1 Branch testing:

python -m coverage run --source=testing/259044798/test/whitebox/branch_testing `
    -m unittest testing.259044798.test.whitebox.branch_testing.branch_testing

Command for Branch testing coverage: 

python -m coverage report -m

2.2 Statement testing:

python -m unittest testing/259044798/test/whitebox/statement_testing/statement_testing.py

Command for statement testing coverage:

python -m coverage report -m

2.3 Loop testing:

python -m unittest testing/259044798/test/whitebox/loop_testing/loop_test.py

2.4 Condition testing:

python -m unittest testing/259044798/test/whitebox/condition_testing/condition_testing.py

2.5 Concolic testing:

coverage run .\testing\259044798\test\whitebox\concolic_testing.py

Command for concolic testing coverage:

coverage report -m --include="testing/259044798/test/whitebox/concolic_testing.py"

----------------------------------------------------------------------------------------------------------------
Testing commands of 259044657 (Pranav):

1. Blackbox testing:

python -m unittest testing/259044657/test/blackbox/category_partition/fn_1_export_answers/test_export_answers.py

python -m unittest testing/259044657/test/blackbox/category_partition/fn_2_certification_quiz/test_certification_quiz.py

python -m unittest testing/259044657/test/blackbox/category_partition/fn_3_menu_features/test_menu_features.py

python -m unittest testing/259044657/test/blackbox/category_partition/fn_4_wrong_answer_quiz/test_wrong_answer_quiz.py

2. Whitebox testing:

2.1 Branch testing:

coverage run --branch -m unittest testing/259044657/test/whitebox/branch_testing/branch_testing.py

Command for Branch testing coverage: 

coverage report -m

2.2 Statement testing:

python -m unittest testing/259044657/test/whitebox/statement_testing/statement_testing.py

Command for statement testing coverage:

coverage report -m

2.3 Loop testing:

python -m unittest testing/259044657/test/whitebox/loop_testing/loop_test.py

2.4 Condition testing:

python -m unittest testing/259044657/test/whitebox/condition_testing/condition_testing.py

2.5 Concolic testing:

python -m unittest discover -s testing/259044657/test/whitebox -p "concolic_testing.py" -v

--------------------------------------------------------------------------------------------------------------------
Testing commands of 259044657 (Sarthak):

1. Blackbox testing:

python -m unittest testing.259023177.test.blackbox.category_partition.fn_1_open_assessment.test_open_assessment -v
 
python -m unittest testing.259023177.test.blackbox.category_partition.fn_2_fifty_fifty_quiz.test_fifty_fifty_quiz -v
 
python -m unittest testing.259023177.test.blackbox.category_partition.fn_3_short_menu.test_short_menu -v
 
python -m unittest testing.259023177.test.blackbox.category_partition.fn_4_quiz_with_summary.test_quiz_with_summary -v
 
python -m unittest testing.259023177.test.blackbox.category_partition.fn_5_delete_reference_link.test_delete_link_for_mcq -v
 
python -m unittest testing.259023177.test.blackbox.category_partition.fn_6_show_user_links.test_show_user_links -v
 
python -m unittest testing.259023177.test.blackbox.category_partition.fn_7_comparison.test_comparison -v
 
python -m unittest testing.259023177.test.blackbox.category_partition.fn_8_export_question.test_export_questions -v 

2. Whitebox testing:

2.1 Branch testing:

python testing\259023177\test\whitebox\branch_testing\branch_testing.py

2.2 Statement testing:

python testing\259023177\test\whitebox\statement_testing\statement_testing.py

2.3 Loop testing:

python -m unittest -v testing.259023177.test.whitebox.loop_testing.loop_testing

2.4 Condition testing:

python testing\259023177\test\whitebox\condition_testing\condition_testing.py

2.5 Concolic testing:

python testing\259023177\test\whitebox\concolic_testing\concolic_testing.py
