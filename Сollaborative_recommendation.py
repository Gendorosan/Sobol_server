import psycopg2
import math

database = psycopg2.connect(database='Sobol', user='postgres', password=' ', host='127.0.0.1', port=5432)
database_cursor = database.cursor()


# Заполнения списка пользоатель - оцененные товары
def create_dependences():
    database_cursor.execute(f"Select * from evaluations")
    dependences = dict()
    for line in database_cursor:
        user = line[2]
        goods = line[3]
        rating = float(line[1])
        if not user in dependences:
            dependences[user] = dict()
        dependences[user][goods] = rating
    return dependences


# Косинусная мера для определения наиболее похожих векторов
def distCosine(vector_a, vector_b):
    def dotProduct(vector_a, vector_b):
        d = 0.0
        for dim in vector_a:
            if dim in vector_b:
                d += vector_a[dim] * vector_b[dim]
        return d

    return dotProduct(vector_a, vector_b) / math.sqrt(dotProduct(vector_a, vector_a)) / math.sqrt(
        dotProduct(vector_b, vector_b))


def makeRecommendation(user_login, user_rates, count_best_users, count_best_products, basket_array):
    coincidence = [(u, distCosine(user_rates[user_login], user_rates[u])) for u in user_rates if u != user_login]
    best_coincidence = sorted(coincidence)[:count_best_users]
    print(f"Most correlated with {user_login} users:")
    for line in best_coincidence:
        print(f"  UserID: {line[0]}  Coeff: {line[1]}")
    sim = dict()
    sim_all = sum([x[1] for x in best_coincidence])
    best_coincidence = dict([x for x in best_coincidence if x[1] > 0.0])
    for related_user in best_coincidence:
        for good in user_rates[related_user]:
            # Проверка на то, чтобы предложенный товар не был в оценках пользователя и в текущей корзине
            if not good in user_rates[user_login] and good not in basket_array:
                if not good in sim:
                    sim[good] = 0.0
                sim[good] += user_rates[related_user][good] * best_coincidence[related_user]
    for good in sim:
        sim[good] /= sim_all
    best_goods = sorted(sim.items())[:count_best_products]
    print("Most correlated products:")
    for good_info in best_goods:
        print(f"  ProductID: {good_info[0]}  CorrelationCoeff: {good_info[1]}")
    return [(x[0], x[1]) for x in best_goods]


def get_collab_rec(client_login, basket_array):
    rec = makeRecommendation(client_login, create_dependences(), 5, 5, basket_array)
    goods = []
    for good in rec:
        database_cursor.execute(f"select name from goods where id = '{good[0]}'")
        name = database_cursor.fetchall()[0][0]
        database_cursor.execute(f"select value from properties where name = 'Цена' and goods_id = {good[0]}")
        price = database_cursor.fetchall()[0][0]
        goods.append({"id": good[0], "name": name, "price": price})

    return goods


print(get_collab_rec('Client32', [2, 123, 3]))
