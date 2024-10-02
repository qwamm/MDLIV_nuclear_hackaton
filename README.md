# CoffeeHub
![image](https://github.com/user-attachments/assets/bd09d73f-5151-4362-82ad-d14af97d3d2f)

**CoffeeHub** - это сервис геймификации в IT-командах, который позволяет повысить мотивацию сотрудников за счёт начисления кружек кофе - внутриигровая валюта, которую можно обменять на мерч. 
Кружки можно получать за активность на репозитории и в корпоративных чатах.

# Наша система  

 ![mdliv_nuclear drawio](https://github.com/user-attachments/assets/9f6638eb-6a62-4506-98c1-c5d26b6dcb1a)

## Модели

### Пользователь
Каждый сотрудник регистрируется на портале. У каждого пользователя есть счётчик кружек кофе, который пополняется от разных действий. Например, новых коммитов или сообщений в чате.  
Каждый пользователь может состоять в одной организации, куда его пригласят. Также авторизованный юзер может прикрепить свой гитхаб профиль.  

### Организация  
Пользователь может создать организацию, в которую можно приглашать других пользователей с помощью системы инвайтов. Каждая организация может прикрепить свой гитхаб репозиторий.  

### Гитхаб профиль  
Используется для гитхаб интеграции. Хранит токен, полученный при OAuth аутентификации. Также он хранит информацию о последних, считанных коммите, пулл реквесте и комментарии.  

### Телеграм профиль  
Используется для телеграм интеграции. Хранит юзер нейм и количество очков за сообщения в корпоративном чате.  

## Гитхаб интеграция  
Как говорилось ранее, пользователь может авторизоваться через гитхаб. Наш гитхаб сервис, получив токен от OAuth приложения, может выполнять запросы к гитхабу. 
Core метод гитхаб интеграции - activity. Он собирает статистику юзера на репозитории организации за последнюю неделю.

**Activity** 
Складывается из коммитов, пулл реквестов, а также комментариев под коммитами. Комментарии анализируются LLM на предмет содержательности и в случае оценки ниже 5 не учитываются.  

**Итоговая формула**  
Подсчёт очков за активность на гитхабе производился по формуле:  
```score = 0.6 * total_commits + good_comments_percentage * total_comments + 0.1 * total_pulls```  

> good_comments_percentage подсчитывается, опираясь на ИИ

## Телеграм интеграция  
Пользователь может получать очки за сообщения в чате телеграмма. Для этого ему необходимо авторизоваться через телеграм. 
На данный момент учитывается только длина сообщения, однако в перспективе также может использоваться LLM для анализа содержания.  

# Запуск и работа сервера  

Перед запуском сервера необходимо создать PostgreSql сервер и создать в нём базу данных с следующими параметрами:  
**database name**: *mdliv_nuclear*  
**PG_USER**: *postgres*  
**PG_PASSWORD**: *pgAdminPassword*  
**PG_PORT**: *5432*  
**PG_HOST**: *localhost*  
> Можно сделать это, например, через pgadmin4.  
> Эти параметры также можно изменить на ваше усмотрение, установив переменные среды в файле ```enviroments.py```

## Запуск бота  Телеграмма
--------------

**Команда запуска**   
```$ python start.py```  

## Отладка сервера  
Для отладки и тестирования всего функционала можно заходить на ```http://127.0.0.1:8080/api/docs```, где в доступной форме можно посылать запросы на сервер и получать ответы.  
![image](https://github.com/user-attachments/assets/ce4251ca-f1b7-4c4e-a760-93f9f13dae6f)

## LLM  
Для того, чтобы сервер задействовал LLM, необходимо скачать желаемую модель в формате ```.gguf```, положить её в каталог ```llm_integration/``` и указать название файла в ```llm_enviroments.py```  
В случае отсутствия модели сервер изменит формулу подсчёта очков и продолжит работу.  
Если несмотря на наличие модели хочется отключить её использование(например для экономии ресурсов), можно изменить переменную окружения ```USE_LLM``` в файле ```enviroments.py```  

## Авторизация гит  
И последнее. Для того, чтобы сервер мог послать пост запрос на гитхаб, нужно создать своё OAuth приложение на гитхабе.  
[Поробнее об этом можно прочитать здесь](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app)  
После создания необходимо будет создать файлы ```client_id.txt``` и ```client_secret.txt``` с параметрами OAuth приложения.  
> Также вы можете изменить REDIRECT_URI на свой в файле enviroments.py, но мы не рекомендуем этого делать  


# Используемые технологии  
## FastAPI  
![image](https://github.com/user-attachments/assets/3cd2fa03-d28b-41fb-9e73-b59b5cb25401)  
> Для Бэкенда.
> Потому что fast и потому что API
## React  
![image](https://github.com/user-attachments/assets/2e16e0a0-96fe-4a88-95dd-794d6a65679d)  
> Для Фронтэнда.
## PyGithub  
![image](https://github.com/user-attachments/assets/a464b233-3d71-4f88-baa4-b847acc3a142)  
> Для интеграции с гитхабом.  
## Aiogram  
![image](https://github.com/user-attachments/assets/d3a1c528-3449-426f-a3aa-9b28021cb17d)  
> Для интеграции с телеграмом.
## Capybarahermes-2.5-mistral-7b.Q3_K_L  
![image](https://github.com/user-attachments/assets/5824f85f-4a4c-42f0-9523-56dd1531027c)
> Как LLM для анализа комментариев на гите.  