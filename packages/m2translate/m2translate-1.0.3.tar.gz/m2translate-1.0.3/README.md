# M2Translate localization / translation package

### Status

[![Build Status](https://travis-ci.org/mdutkin/m2translate.svg?branch=master)](https://travis-ci.org/mdutkin/m2translate)


### About


M2Translate is a package for localization / translation everything you want in your Python projects. 
You can store all your translations in JSON files or Redis. Once initialised, it sits in a memory until 
you save it to store.

The main concept is that you have a bunch of locales, and each of them has it's own set of placeholders. 
Placeholders are synchronised while dumping to store. Each placeholder has three values: `none`, `single`, 
`multi`. When you put placeholder somewhere and try to get it's value - you simply get `none` value. But if you 
specify a numeric value - you get placeholder value depending on it (`none` for `0`, `single` for `1` and `multi` 
for `> 1`).


### The list of main features:

* **supports JSON store and Redis store. You can add support of any store you want by implementing 
`StoreConnector` interface**

* **as fast as your RAM**

* **great API offers you methods to modify existing locales and placeholders**

* **have nice docs**


### How-to

Init your connector:

```python
# json
connector = JSONConnector('path/to/your/json_store')

# redis
redis_host = '127.0.0.1'
redis_port = 6379
redis_db = 0
connector = RedisConnector(redis_host=redis_host, redis_port=redis_port, redis_db=redis_db)
```

Init core:

```python
tr = M2Translate(connector, not_found_val='PH NOT FOUND')
```

You can clear all your store:

```python
tr.clear_store()
```

First, add locale (you can even dump all you store to synchronize placeholders between locales):

```python
tr.add_locale('ru_RU', dump_permanently=False)
```

Set a few placeholders to the CURRENT LOCALE:

```python
tr.set_p('FORM1.NAME', none='Имя')
tr.set_p('FORM1.VISITS', none='визитов', single='визит', multi='визитов')
# or like that - to a different locale
tr.set_p('FORM1.VISITS', none='визитов', single='визит', multi='визитов', l='ru_RU')
```

Add another locale and set it as current:

```python
tr.add_locale('en_US', dump_permanently=False)
tr.set_cur_locale('en_US')
```

And also add a value for placeholder:

```python
tr.set_p('FORM1.NAME', none='Name')
tr.set_p('FORM1.VISITS', none='visits', single='visit', multi='visits')
```

Save everything you have in RAM to store:

```python
tr.dump_locales()
```

Reload your store in RAM (maybe there are some changes in the remote store?):

```python
tr.reload_locales()
```

Check current locale:

```python
print(tr.locale)
```

Or remove useless locale:

```python
tr.remove_locale('en_US', dump_permanently=True)
```

It's time to get our values:

```python
name = input(tr.p('FORM1.NAME'))
visits = 10
print('%s: %s %s' % (name, visits, tr.p('FORM1.VISITS', visits)))
```

### Example

You can try example in `example/live_example.py`, or take a view at tests.

Let's see the example output for `example/live_example.py` in different locales:

```bash
select locale from the following list ['ru_RU', 'en_US', 'fr_FR']: ru_RU
Для того, чтобы увидеть демку, заполните следующие данные
Ваше имя: Максим
Ваша фамилия: Дуткин
Сколько вам лет: 28
Отлично, теперь посмотри, что получилось!
Спасибо, что ты проявил интерес к этому пакету. Сегодня `четверг,  1 марта 2018 г. 23:57:29` (проверка даты локали), тебя зовут Максим Дуткин и тебе сейчас 28 лет!
```

```bash
select locale from the following list ['ru_RU', 'en_US', 'fr_FR']: en_US
For demo purposes, fill data below
Your name: Maxim
Your surname: Dutkin
How old are you: 28
Awesome, check out the output!
Great that you showed interest to this package. Today is `Fri Mar  2 00:13:36 2018` (locale date check), your fullname is Maxim Dutkin and you are 28 years old!
```

```bash
select locale from the following list ['ru_RU', 'en_US', 'fr_FR']: fr_FR
Pour des fins de démonstration, remplissez les données ci-dessous
Votre nom: Maxim
Votre nom de famille: Dutkin
Quel âge avez-vous: 28
Génial, consultez la sortie!
Génial que vous avez montré de l'intérêt pour ce package. Aujourd'hui est `Ven  2 mar 00:14:45 2018` (vérification de la date locale), votre nom complet est Maxim Dutkin et vous avez 28 ans!
``