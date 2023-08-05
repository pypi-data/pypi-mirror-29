# NuQui extension
This is a little module to make chatbots able to ask questions. There is already a prototype that uses the NuQui module [you find it here](https://github.com/nuqui-chatbot/nuqui-nombot). It has over 200 Questions about food in German. You can easily change the sqlite database to add more questions or adapt them to your needs. (it will never ask the same questions twice).

The question will be related to the food that the user ate. If there are no meal entry it will ask a random question.

### Installation
The installation is quite easy. It is a pypi module so you can just install it via pip.
```
pip install nuqui
```

If you want to install it form source code you just have to clone the, move into the root directory and then run the following command:
```
pip install -r requirements.txt
python setup.py install
```

### Usage
Nuqui is quite easy to use and has just a few methods to invoke in your program.

First you need to import nuqui in the file you need it
```
import nuqui
```
#### USer Management
After the import we need to make a new user in the nuqui module so we have to call 
```
nuqui.create_user(<user_id>, <name>)
```
If your bot or program has the possibility to delete a user you have can also delete the user in the nuqui module by calling
```
nuqui.delete_user(<user_id>)
```
This will delete the user and everyhting related to him.

#### add meals
Then we need to add a meal to the user. That is also pretty simple to do. Just call 
```
nuqui.add_meal(<user_id>, <food_String>, <total_calories>)
```
The 'food_string' needs to have a certain format. Just use ingredents of the meal and then concatenate them together with a comma seperation. e.g. "wasser,apfel,salz". The total calories are an int that represents the total calories of the whole meal.

#### Get a Question
Now as you have some restriction in the database you can ask for a question. With 
```
nuqui.get_predefined_question_dict_with_random_answers(<user_id>)
```
you get a question dictionary (JSON) with the following structure:
```
{
  "question": questionstring,
  "answer": an array with 4 answer options,
  "value": the points you get for this question
}
```
Let your user answer with 4 options (!A, !B, !C, !D)

#### Evaluate your answer
Because you dont know what the right answer you need e evaluation.
```
nuqui.evaluat(<answer>, <user_id>)
```
This function need an answer (A sting that contains either !A, !B, !C or !D) and the user id. It will return you a Dictornary (JSON) in the following structur:

```
{
  "success": boolean,
  "right_answer": right_answer,
  "achieved_points": points the question was worth,
  "total_points": the total points of the user
  }
```

### run tests
You can also test the module by running the tests in the tests folder. They are all based on the standart unit test python framework.
To run the tests just type
```
python tests/test_basic.py
```

### Future work
* delete question form the user after a certain time
* make the database more persistent
