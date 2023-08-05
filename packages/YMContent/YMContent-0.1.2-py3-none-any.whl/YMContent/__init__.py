# -*- coding: utf-8 -*-


import socket
import ssl

import requests
from requests.exceptions import ConnectionError, ReadTimeout, SSLError

from .constants import *
from .exceptions import *
from .response import *

__title__ = 'YMContent'
__version__ = constants.VERSION
__author__ = 'Pavel Yegorov'
__license__ = 'Apache 2.0'


class YMAPI(object):
    """

    :param authorization_key: Авторизационный ключ
    :type authorization_key: str
    """

    def __init__(self, authorization_key=None):
        if not authorization_key:
            raise NotAuthorized(
                "You must provide authorization key to access Yandex.Market API!")
        self.session = requests.Session()
        self.session.headers = {
            'Host': DOMAIN,
            'Authorization': authorization_key,
            'User-agent': USER_AGENT,
        }

    def _request(self, resource, req_id, params):
        if resource not in RESOURCES:
            raise Exception('Resource "%s" unsupported' % resource)

        resource_path = resource.format(req_id)
        url = '{}://{}/{}/{}'.format(PROTOCOL, DOMAIN, API_VERSION, resource_path)

        try:
            r = self.session.get(
                url=url,
                params=params
            )

            data = r.json()

            if r.status_code in (401, 404, 422):
                raise BaseAPIError(
                    data['errors'][0]['message'])
            return r

        except (ConnectionError, ReadTimeout, SSLError, ssl.SSLError,
                socket.error) as exception:
            pass

    @staticmethod
    def _validate_fields(fields, values):
        if type(fields) == list:
            for field in fields:
                if field.upper() not in values:
                    raise FieldsParamError('"fields" param is wrong')
        elif type(fields) == str:
            for field in fields.split(','):
                if field.strip() not in values:
                    raise FieldsParamError('"fields" param is wrong')
        else:
            raise FieldsParamError('"fields" param is wrong')
        return fields

    def categories(self, fields=None, sort='NONE', geo_id=None, remote_ip=None, count=10, page=1):
        """
        Список категорий

        :param fields: Параметры категории, которые необходимо показать в выходных данных:

            * **PARENT** — информация о родительской категории
            * **STATISTICS** — статистика по категории. Например, количество моделей и товарных предложений в категории
            * **WARNINGS** — предупреждения, связанные с показом категории
            * **ALL** - Все значения

            .. note:: Значение ALL доступно только для отладки и имеет ограничение по нагрузке – один RPS

        :type fields: str or list[str]

        :param sort: Тип сортировки категорий:

            * **BY_NAME** — сортировка категорий в алфавитном порядке
            * **BY_OFFERS_NUM** — сортировка по количеству товарных предложений в каждой категории
            * **NONE** — сортировка по умолчанию

        :type sort: str

        :param geo_id: Идентификатор региона
        :type geo_id: int or str

        :param remote_ip: IP-адрес пользователя
        :type remote_ip: str

        :param count: Количество выводимых результатов на странице ответа
        :type count: int

        :param page: Номер страницы
        :type page: int

        :return: Список категорий первого уровня (корневых) товарного дерева
        :rtype: response.Categories

        :raises FieldsParamError: неверное значение параметра fields
        :raises SortParamError: неверное значение параметра sort
        :raises NoGeoIdOrIP: не передан обязательный параметр geo_id или remote_ip
        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page

        .. seealso:: https://tech.yandex.ru/market/content-data/doc/dg-v2/reference/category-controller-v2-get-root-categories-docpage/
        """
        params = {}

        if fields:
            params['fields'] = self._validate_fields(fields, constants.CATEGORY_FIELDS)

        if sort:
            if sort.upper() not in constants.CATEGORY_SORT:
                raise SortParamError('"sort" param is wrong')
            params['sort'] = sort

        if geo_id is None and remote_ip is None:
            raise NoGeoIdOrIP(
                "You must provide either geo_id or remote_ip")

        if geo_id:
            params['geo_id'] = geo_id

        if remote_ip:
            params['remote_ip'] = remote_ip

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        return Categories(self._request('categories', None, params))

    def categories_children(self, category_id, fields=None, sort='NONE', geo_id=None, remote_ip=None, count=10,
                            page=1):
        """
        Список подкатегорий

        :param category_id: Идентификатор категории
        :type category_id: int or str

        :param fields: Параметры категории, которые необходимо показать в выходных данных:

            * **PARENT** — информация о родительской категории
            * **STATISTICS** — статистика по категории. Например, количество моделей и товарных предложений в категории
            * **WARNINGS** — предупреждения, связанные с показом категории
            * **ALL** - Все значения

            .. note:: Значение ALL доступно только для отладки и имеет ограничение по нагрузке – один RPS

        :type fields: str or list[str]

        :param sort: Тип сортировки категорий:

            * **BY_NAME** — сортировка категорий в алфавитном порядке
            * **BY_OFFERS_NUM** — сортировка по количеству товарных предложений в каждой категории
            * **NONE** — сортировка по умолчанию

        :type sort: str

        :param geo_id: Идентификатор региона
        :type geo_id: int or str

        :param remote_ip: IP-адрес пользователя
        :type remote_ip: str

        :param count: Количество выводимых результатов на странице ответа
        :type count: int

        :param page: Номер страницы
        :type page: int

        :return: Список категорий товарного дерева, вложенных в категорию с указанным в запросе идентификатором
        :rtype: response.CategoriesChildren

        :raises FieldsParamError: неверное значение параметра fields
        :raises SortParamError: неверное значение параметра sort
        :raises NoGeoIdOrIP: не передан обязательный параметр geo_id или remote_ip
        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page

        .. seealso:: https://tech.yandex.ru/market/content-data/doc/dg-v2/reference/category-controller-v2-get-children-categories-docpage/
        """
        params = {}
        if geo_id is None and remote_ip is None:
            raise NoGeoIdOrIP(
                "You must provide either geo_id or remote_ip")
        if geo_id:
            params['geo_id'] = geo_id

        if remote_ip:
            params['remote_ip'] = remote_ip

        if fields:
            params['fields'] = self._validate_fields(fields, constants.CATEGORY_FIELDS)

        if sort:
            if sort not in constants.CATEGORY_SORT:
                raise SortParamError('"sort" param is wrong')
            params['sort'] = sort

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        return Categories(self._request('categories/{}/children', category_id, params))

    def category(self, category_id, fields=None, geo_id=None, remote_ip=None):
        """
        Информация о категории

        :param category_id: Идентификатор категории
        :type category_id: int or str

        :param fields: Параметры категории, которые необходимо показать в выходных данных:

            * **PARENT** — информация о родительской категории
            * **STATISTICS** — статистика по категории. Например, количество моделей и товарных предложений в категории
            * **WARNINGS** — предупреждения, связанные с показом категории
            * **ALL** - Все значения

            .. note:: Значение ALL доступно только для отладки и имеет ограничение по нагрузке – один RPS

        :type fields: str or list[str]

        :param geo_id: Идентификатор региона
        :type geo_id: int or str

        :param remote_ip: IP-адрес пользователя
        :type remote_ip: str

        :return: Информация о категории
        :rtype: response.Category

        :raises NoGeoIdOrIP: не передан обязательный параметр geo_id или remote_ip
        :raises FieldsParamError: неверное значение параметра fields

        .. seealso:: https://tech.yandex.ru/market/content-data/doc/dg-v2/reference/category-controller-v2-get-category-docpage/
        """
        params = {}
        if geo_id is None and remote_ip is None:
            raise NoGeoIdOrIP(
                "You must provide either geo_id or remote_ip")
        if geo_id:
            params['geo_id'] = geo_id

        if remote_ip:
            params['remote_ip'] = remote_ip

        if fields:
            params['fields'] = self._validate_fields(fields, constants.CATEGORY_FIELDS)

        return Category(self._request('categories/{}', category_id, params))

    def categories_filters(self, category_id, geo_id=None, remote_ip=None, fields=None, filter_set='POPULAR',
                           rs=None,
                           sort='NONE', filters=None):
        """
        Список фильтров категории

        :param category_id: Идентификатор категории
        :type category_id: int or str

        :param fields: Параметры категории, которые необходимо показать в выходных данных:

            * **ALLVENDORS** — группа параметров для фильтра «Производитель
            * **DESCRIPTION** — описания фильтров
            * **FOUND** — количество моделей или товарных предложений
            * **SORTS** — включение в выдачу доступных фильтров
            * **STANDARD** = ALLVENDORS, DESCRIPTION, FOUND, SORTS
            * **ALL** - Все значения

            .. note:: Значение ALL доступно только для отладки и имеет ограничение по нагрузке – один RPS

        :type fields: str or list[str]

        :param geo_id: Идентификатор региона
        :type geo_id: int or str

        :param remote_ip: IP-адрес пользователя
        :type remote_ip: str

        :param filter_set: Набор фильтров в выходных данных:

            * **ALL** — все фильтры
            * **BASIC** — базовый набор фильтров
            * **POPULAR** — только популярные фильтры

            .. note:: Значение BASIC равнозначно POPULAR

        :type filter_set: str

        :param rs: Поле содержащее закодированную информацию о текстовом запросе после редиректа, на которую будет ориентироваться поиск
        :type rs: str

        :param sort: Тип сортировки категорий:

            * **NAME** — сортировка по имени
            * **NONE** — сортировка отсутствует

        :type sort: str

        :param filters: Условия фильтрации моделей и предложений на модель
        :type filters: dict

        :return: Cписок фильтров для фильтрации моделей и товарных предложений в указанной категории
        :rtype: response.Filters

        :raises NoGeoIdOrIP: не передан обязательный параметр geo_id или remote_ip
        :raises FieldsParamError: неверное значение параметра fields
        :raises FilterSetParamError: неверное значение параметра filter_set
        :raises SortParamError: неверное значение параметра sort

        .. seealso:: https://tech.yandex.ru/market/content-data/doc/dg-v2/reference/category-controller-v2-get-category-filters-docpage/
        """
        params = {}
        if geo_id is None and remote_ip is None:
            raise NoGeoIdOrIP(
                "You must provide either geo_id or remote_ip")
        if geo_id:
            params['geo_id'] = geo_id

        if remote_ip:
            params['remote_ip'] = remote_ip

        if fields:
            params['fields'] = self._validate_fields(fields, constants.SEARCH_FILTERS)

        if filter_set:
            for field in filter_set.split(','):
                if field not in constants.FILTER_SET:
                    raise FilterSetParamError('"filter_set" param is wrong')
            params['filter_set'] = filter_set

        if sort:
            if sort not in ('NAME', 'NONE'):
                raise SortParamError('"sort" param is wrong')
            params['sort'] = sort

        if rs:
            params['rs'] = rs

        if filters:
            for (k, v) in filters.items():
                params[k] = v

        return Filters(self._request('categories/{}/filters', category_id, params))

    def categories_match(self, name, category_name=None, description=None, locale='RU_ru', price=None,
                         shop_name=None):
        """
        Подбор категорий по параметрам

        :param name: Имя
        :type name: str

        :param category_name: Наименование категории
        :type category_name: str

        :param description: Описание модели
        :type description: str

        :param locale: Локаль поиска
        :type locale: str

        :param price: Цена модели
        :type price: str or int

        :param shop_name: Наименование магазина
        :type shop_name: str

        :return: Подобранные категории
        :rtype: response.Category

        .. seealso:: https://tech.yandex.ru/market/content-data/doc/dg-v2/reference/category-controller-v2-match-docpage/
        """
        params = {'name': name, 'locale': locale}

        if category_name:
            params['category_name'] = category_name

        if description:
            params['description'] = description

        if price:
            params['price'] = price

        if shop_name:
            params['shop_name'] = shop_name

        return Category(self._request('categories/match', None, params))

    def model(self, model_id, fields='CATEGORY,PHOTO', filters=None, geo_id=None, remote_ip=None):
        """
        Информация о модели

        :param model_id: Идентификатор модели
        :type model_id: int or str

        :param fields: Свойства модели, которые необходимо показать в выходных данных:

            * **CATEGORY** — Информация о категории, к которой относится модель
            * **DEFAULT_OFFER** — информация о товарном предложении по умолчанию для модели в указанном регионе.
            * **DISCOUNTS** — информация о скидках на модель.
            * **FACTS** — Список достоинств и недостатков модели
            * **FILTERS** — список фильтров, доступных для отбора модификаций модели.
            * **FILTER_ALLVENDORS** — группа параметров для фильтра «Производитель».
            * **FILTER_COLOR** — список фильтров по цвету, доступных для отбора модификаций модели.
            * **FILTER_DESCRIPTION** — описания фильтров.
            * **FILTER_FOUND** — количество моделей или товарных предложений:
            * **FILTER_SORTS** — включение в выдачу доступных фильтров.
            * **MEDIA** — информация об отзывах и обзорах на модель.
            * **MODIFICATIONS** — краткая информация о модификациях (для групповой модели).
            * **NAVIGATION_NODE** — информация о навигационном узле дерева категорий Маркета, к которому относится модель.
            * **NAVIGATION_NODE_DATASOURCE** — источник данных узла навигационного дерева.
            * **NAVIGATION_NODE_ICONS** — иконки навигационного дерева.
            * **NAVIGATION_NODE_STATISTICS** — статистика узла навигационного дерева.
            * **OFFERS** — информация о товарных предложениях, соотнесенных с моделью, в указанном регионе.
            * **OFFER_ACTIVE_FILTERS** — активные фильтры.
            * **OFFER_CATEGORY** — информация о категории предложения.
            * **OFFER_DELIVERY** — информация о доставке.
            * **OFFER_DISCOUNT** — скидка.
            * **OFFER_OFFERS_LINK** — Ссылка на страницу с офферами для той же модели в том же магазине.
            * **OFFER_OUTLET** — информация о точке выдачи производетеля.
            * **OFFER_PHOTO** — фото предложения.
            * **OFFER_SHOP** — магазин от которого поступило предложенение.
            * **OFFER_VENDOR** — информация о поставщике.
            * **PHOTO** — Изображение модели, используемое как основное изображение на карточке модели
            * **PHOTOS** — все доступные изображения модели.
            * **PRICE** — информация о ценах на модель.
            * **RATING** — иформация о рейтинге и оценках модели.
            * **SHOP_ORGANIZATION** — юридическая информация: юридический и фактический адрес, ОГРН, тип организации, ссылка на реквизиты.
            * **SHOP_RATING** — рейтинг магазина.
            * **SPECIFICATION** — характеристики модели.
            * **VENDOR** — информация о производителе.
            * **ALL** = Все значения
            * **FILTER_ALL** = FILTER_ALLVENDORS, FILTER_DESCRIPTION, FILTER_FOUND, FILTER_SORTS
            * **NAVIGATION_NODE_ALL** = NAVIGATION_NODE_DATASOURCE, NAVIGATION_NODE_ICONS, NAVIGATION_NODE_STATISTICS
            * **OFFER_ALL** = OFFER_ACTIVE_FILTERS, OFFER_BUNDLE_SETTINGS, OFFER_CATEGORY, OFFER_DELIVERY, OFFER_DISCOUNT, OFFER_LINK, OFFER_OFFERS_LINK, OFFER_OUTLET, OFFER_PHOTO, OFFER_SHOP, OFFER_VENDOR
            * **SHOP_ALL** = SHOP_ORGANIZATION, SHOP_RATING
            * **STANDARD** = CATEGORY, OFFERS, OFFER_CATEGORY, OFFER_DELIVERY, OFFER_OUTLET, OFFER_PHOTO, OFFER_SHOP, PHOTO, PRICE, RATING, SHOP_RATING, VENDOR
            * **VENDOR_ALL** = VENDOR_LINK

            .. note:: Значение ALL доступно только для отладки и имеет ограничение по нагрузке – один RPS

        :type fields: str or list[str]

        :param filters: Условия фильтрации моделей и предложений на модель
        :type filters: dict

        :param geo_id: Идентификатор региона
        :type geo_id: int or str

        :param remote_ip: IP-адрес пользователя
        :type remote_ip: str

        :return: Информация о модели
        :rtype: response.Model

        :raises NoGeoIdOrIP: не передан обязательный параметр geo_id или remote_ip
        :raises FieldsParamError: неверное значение параметра fields

        .. seealso:: https://tech.yandex.ru/market/content-data/doc/dg-v2/reference/models-controller-v2-get-model-docpage/
        """
        params = {}
        if geo_id is None and remote_ip is None:
            raise NoGeoIdOrIP(
                "You must provide either geo_id or remote_ip")
        if geo_id:
            params['geo_id'] = geo_id

        if remote_ip:
            params['remote_ip'] = remote_ip

        if fields:
            params['fields'] = self._validate_fields(fields, constants.MODEL_FIELDS)

        if filters:
            for (k, v) in filters.items():
                params[k] = v

        return Model(self._request('models/{}', model_id, params))

    def models_reviews(self, model_id, count=10, page=1):
        """
        Список обзоров на модель

        :param model_id: Идентификатор модели
        :type model_id: int or str

        :param count: Количество элементов на странице
        :type count: int

        :param page: Номер страницы
        :type page: int

        :return: Обзоры на модель
        :rtype: response.ModelReview

        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page

        .. seealso:: https://tech.yandex.ru/market/content-data/doc/dg-v2/reference/models-controller-v2-get-reviews-docpage/
        """
        params = {}
        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        return ModelReview(self._request('models/{}/reviews', model_id, params))

    def models_match(self, name, category_count=1, fields='CATEGORY,PHOTO', match_types='MULTI,REPORT',
                     category_name=None, description=None, locale='RU_ru', price=None, shop_name=None, category_id=None,
                     hid=None):
        """
        Поиск модели по названию и параметрам

        :param name: Имя
        :type name: str

        :param category_count: Количество категорий
        :type category_count: int

        :param fields: Параметры моделей, которые необходимо показать в выходных данных
        :type fields: str or list

        :param match_types: Типы поиска
        :type match_types: str or list

        :param category_name: Наименование категории
        :type category_name: str

        :param description: Описание модели
        :type description: str

        :param locale: Локаль поиска
        :type locale: str

        :param price: Цена модели
        :type price: str or int

        :param shop_name: Наименование магазина
        :type shop_name: str

        :param category_id: Идентификаторы категорий
        :type category_id: list[int]

        :param hid: Идентификаторы категорий
        :type hid: list[int]

        :return: Модель из гуризованной категории по названию и параметрам, удовлетворяющим заданным во входных данных условиям поиска
        :rtype: response.Models

        :raises FieldsParamError: недопустимое значение параметра fields
        :raises MatchTypeParamError: недопустимое значение параметра match_types

        .. seealso:: https://tech.yandex.ru/market/content-data/doc/dg-v2/reference/models-controller-v2-get-matched-models-docpage/
        """
        params = {'category_count': category_count,
                  'fields': fields,
                  'match_types': match_types,
                  'name': name, 'locale': locale}

        if fields:
            params['fields'] = self._validate_fields(fields, constants.MODEL_FIELDS)

        if match_types:
            for match_type in match_types.split(','):
                if match_type not in (
                        'BATCH', 'MULTI', 'MULTI_STRING', 'REPORT', 'STRING', 'ALL'):
                    raise MatchTypeParamError('"match_types" param is wrong')

        if category_name:
            params['category_name'] = category_name

        if description:
            params['description'] = description

        if price:
            params['price'] = price

        if shop_name:
            params['shop_name'] = shop_name

        if category_id:
            params['category_id'] = category_id

        if hid:
            params['hid'] = hid

        return Models(self._request('models/match', None, params))

    def models_lookas(self, model_id, count=10, page=1, fields='CATEGORY,PHOTO'):
        """
        Список похожих моделей

        :param model_id: Идентификатор модели
        :type model_id: int or str

        :param count: Количество элементов на странице
        :type count: int

        :param page: Номер страницы
        :type page: int

        :param fields: Параметры моделей, которые необходимо показать в выходных данных
        :type fields: str or list[str]

        :return: Cписок моделей, которые похожи на указанную в запросе
        :rtype: response.Models

        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page
        :raises FieldsParamError: недопустимое значение параметра fields

        .. seealso:: https://tech.yandex.ru/market/content-data/doc/dg-v2/reference/models-controller-v2-get-matched-models-docpage/
        """
        params = {}

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        if fields:
            params['fields'] = self._validate_fields(fields, constants.MODEL_FIELDS)

        return Models(self._request('models/{}/looksas', model_id, params))

    def categories_bestdeals(self, category_id, fields='CATEGORY,PHOTO', count=10, page=1):
        """
        Лучшие предложения (скидки дня)

        :param category_id: Идентификатор категории
        :type category_id: int or str

        :param count: Количество элементов на странице
        :type count: int

        :param page: Номер страницы
        :type page: int

        :param fields: Параметры моделей, которые необходимо показать в выходных данных
        :type fields: str or list[str]

        :return:
        :rtype: response.CategoriesLookas

        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page
        :raises FieldsParamError: недопустимое значение параметра fields

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/category-controller-v2-get-best-deals-docpage/
        """
        params = {'fields': fields}

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        if fields:
            params['fields'] = self._validate_fields(fields, constants.MODEL_FIELDS)

        return CategoriesLookas(self._request('categories/{}/bestdeals', category_id, params))

    def categories_popular(self, category_id, fields='CATEGORY,PHOTO', count=10, page=1, geo_id=None, remote_ip=None):
        """
        Список популярных моделей

        :param category_id: Идентификатор категории
        :type category_id: int or str

        :param count: Количество элементов на странице
        :type count: int

        :param page: Номер страницы
        :type page: int

        :param fields: Параметры моделей, которые необходимо показать в выходных данных
        :type fields: str or list[str]

        :param geo_id: Идентификатор региона
        :type geo_id: int or str

        :param remote_ip: Идентификатор региона пользователя
        :type remote_ip: str

        :return: популярные на Яндекс.Маркете модели
        :rtype: response.Models

        :raises NoGeoIdOrIP: не передан обязательный параметр geo_id или remote_ip
        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page
        :raises FieldsParamError: недопустимое значение параметра fields

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/category-controller-v2-get-popular-models-docpage/
        """
        params = {}

        if geo_id is None and remote_ip is None:
            raise NoGeoIdOrIP(
                "You must provide either geo_id or remote_ip")
        if geo_id:
            params['geo_id'] = geo_id

        if remote_ip:
            params['remote_ip'] = remote_ip

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        if fields:
            params['fields'] = self._validate_fields(fields, constants.MODEL_FIELDS)

        return Models(self._request('categories/{}/populars', category_id, params))

    def model_offers(self, model_id, delivery_included=False, fields=None, group_by=None, shop_regions=None,
                     filters=None,
                     count=10, page=1, how=None, sort=None, latitude=None, longitude=None):
        """
        Список предложений на модель

        :param model_id: Идентификатор модели
        :type model_id: int or str

        :param delivery_included: Признак включения цены доставки в цену товарного предложения
        :type delivery_included: bool or int or str

        :param fields: Параметры товарных предложений, которые необходимо показать в выходных данных
        :type fields: str or list[str]

        :param group_by: Вариант группировки товарных предложений
        :type group_by: str

        :param shop_regions: Идентификаторы регионов магазинов
        :type shop_regions: str or list[int]

        :param filters: Параметры задают условия фильтрации моделей и предложений на модель
        :type filters: dict

        :param count: Количество элементов на странице
        :type count: int

        :param page: Номер страницы
        :type page: int

        :param how: Направление сортировки
        :type how: str

        :param sort: Тип сортировки товарных предложений:

            * **DATE** — сортировка по дате
            * **DELIVERY_TIME** — сортировка по времени доставки
            * **DISCOUNT** — сортировка по размеру скидки
            * **DISTANCE** — сортировка по расстоянию до ближайшей точки продаж (значение доступно только при указании местоположения пользователя)
            * **NOFFERS** — сортировка по количеству предложений
            * **OPINIONS** — сортировка по количеству отзывов
            * **POPULARITY** — сортировка по популярности
            * **PRICE** — сортировка по цене
            * **QUALITY** — сортировка по рейтингу
            * **RATING** — сортировка по рейтингу
            * **RELEVANCY** — сортировка по релевантности

        :type sort: str

        :param latitude: Широта
        :type latitude: int or str or float

        :param longitude: Долгота
        :type longitude: int or str or float

        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page
        :raises DeliveryIncludedParamError: недопустимое значение параметра delivery_included
        :raises FieldsParamError: недопустимое значение параметра fields
        :raises GroupByParamError: недопустимое значение параметра group_by
        :raises HowParamError: недопустимое значение параметра how
        :raises SortParamError: недопустимое значение параметра sort
        :raises GeoParamError: недопустимое значение параметра latitude
        :raises GeoParamError: недопустимое значение параметра longitude

        :return: Список товарных предложений, соотнесенных с указанной моделью
        :rtype: response.ModelOffers

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/models-controller-v2-get-offers-docpage/
        """
        params = {}

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        if delivery_included:
            if str(delivery_included).upper() in [0, '0', 'F', 'FALSE', 'N', 'NO']:
                delivery_included = 'FALSE'
            elif str(delivery_included).upper() in [1, '1', 'T', 'TRUE', 'Y', 'YES']:
                delivery_included = 'TRUE'
            else:
                raise DeliveryIncludedParamError('"delivery_included" param is wrong')
            params['delivery_included'] = delivery_included

        if fields:
            params['fields'] = self._validate_fields(fields,
                                                     (
                                                         'FILTERS', 'FILTER_ALLVENDORS',
                                                         'FILTER_DESCRIPTION', 'FILTER_FOUND', 'FILTER_SORTS',
                                                         'OFFER_ACTIVE_FILTERS', 'OFFER_CATEGORY', 'OFFER_DELIVERY',
                                                         'OFFER_DISCOUNT',
                                                         'OFFER_OFFERS_LINK', 'OFFER_OUTLET', 'OFFER_OUTLET_COUNT',
                                                         'OFFER_PHOTO', 'OFFER_SHOP', 'OFFER_VENDOR',
                                                         'SHOP_ORGANIZATION', 'SHOP_RATING', 'SORTS', 'ALL',
                                                         'FILTER_ALL',
                                                         'OFFER_ALL', 'SHOP_ALL', 'STANDARD', 'VENDOR_ALL'))

        if group_by:
            if group_by not in ('NONE', 'OFFER', 'SHOP'):
                raise GroupByParamError('"group_by" param is wrong')
            params['group_by'] = group_by

        if shop_regions:
            params['shop_regions'] = shop_regions

        if filters:
            for (k, v) in filters.items():
                params[k] = v

        if how:
            if how not in ('ASC', 'DESC'):
                raise HowParamError('"how" param is wrong')

        if sort:
            if sort not in constants.MODEL_SORT:
                raise SortParamError('"sort" param is wrong')
            params['sort'] = sort

        # Todo Ограничение. Для sort=DISCOUNT возможна только сортировка по убыванию (how=DESC).

        # todo Ограничение. Оба парметра должны быть определены совместно. Не допускается указывать один без другого.

        if latitude:
            if latitude < -90 or latitude > 90:
                raise GeoParamError('"latitude" param must be between -90 and 90')
            params['latitude'] = latitude

        if longitude:
            if longitude < -180 or longitude > 180:
                raise GeoParamError('"longitude" param must be between -180 and 180')
            params['longitude'] = longitude

        return ModelOffers(self._request('models/{}/offers', model_id, params))

    def model_offers_default(self, model_id, fields='STANDARD', filters=None):
        """
        Товарное предложение по умолчанию

        :param model_id: Идентификатор модели
        :type model_id: int or str

        :param fields: Параметры предложений, которые необходимо показать в выходных данных

            * **ACTIVE_FILTERS** — активные фильтры
            * **CATEGORY** — информация о категории предложения
            * **DELIVERY** — информация о доставке
            * **DISCOUNT** — скидка
            * **OFFERS_LINK** — Ссылка на страницу с офферами для той же модели в том же магазине
            * **OUTLET** — информация о точке выдачи производетеля
            * **OUTLET_COUNT** — Количество точек выдачи предложени
            * **PHOTO** — фото предложения
            * **SHOP** — магазин от которого поступило предложенение
            * **SHOP_ORGANIZATION** — юридическая информация: юридический и фактический адрес, ОГРН, тип организации, ссылка на реквизиты
            * **SHOP_RATING** — рейтинг магазина
            * **VENDOR** — информация о поставщике
            * **ALL** = Все значения
            * **SHOP_ALL** = SHOP_ORGANIZATION, SHOP_RATING
            * **STANDARD** = CATEGORY, DELIVERY, OUTLET, OUTLET_COUNT, PHOTO, SHOP, SHOP_RATING

        :type fields: str or list[str]

        :param filters: Параметры задают условия фильтрации моделей и предложений на модель
        :type filters: dict

        :raises FieldsParamError: недопустимое значение параметра fields

        :return: Товарное предложение по умолчанию
        :rtype: response.ModelOffersDefault

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/models-controller-v2-get-default-offer-docpage/
        """
        params = {}

        if fields:
            params['fields'] = self._validate_fields(fields, constants.OFFER_FIELDS)

        if filters:
            for (k, v) in filters.items():
                params[k] = v

        return ModelOffersDefault(self._request('models/{}/offers/default', model_id, params))

    def model_offers_stat(self, model_id):
        """
        Количество товарных предложений на модель по регионам
        :param model_id: Идентификатор модели
        :type model_id: int or str

        :return: Информация о количестве товарных предложений на указанную модель по регионам, а также минимальную, максимальную и среднюю стоимость этой модели
        :rtype: response.ModelOffersStat

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/models-controller-v2-get-model-offers-stat-docpage/
        """
        params = {}

        return ModelOffersStat(self._request('models/{}/offers/default', model_id, params))

    def model_offers_filters(self, model_id, fields=None, filter_set=None, sort='NONE'):
        """
        Список фильтров для предложений на модель

        :param model_id: Идентификатор модели
        :type model_id: int or str

        :param fields: Группы параметров, которые необходимо отобразить в выходных данных
        :type fields: str or list[str]

        :param filter_set: Набор фильтров в выходных данных:

            * **ALL** — все фильтры
            * **BASIC** — базовый набор фильтров
            * **POPULAR** — только популярные фильтры

            .. note:: Значение BASIC равнозначно POPULAR

        :type filter_set: str

        :param sort: Задает тип сортировки значений в фильтрах
        :type sort: str

        :raises FieldsParamError: недопустимое значение параметра fields
        :raises FilterSetParamError: недопустимое значение параметра filter_set
        :raises SortParamError: недопустимое значение параметра sort

        :return: Cписок фильтров и сортировок, доступных для фильтрации и сортировки товарных предложений указанной модели
        :rtype: response.Filters

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/models-controller-v2-get-model-offers-filters-docpage/
        """
        params = {}

        if fields:
            params['fields'] = self._validate_fields(fields,
                                                     constants.SEARCH_FILTERS)

        if filter_set:
            if filter_set not in constants.FILTER_SET:
                raise FilterSetParamError('"filter_set" param is wrong')
            params['filter_set'] = filter_set

        if sort:
            if sort not in ('NAME', 'NONE'):
                raise SortParamError('"sort" param is wrong')

        return Filters(self._request('models/{}/offers/filters', model_id, params))

    def offer(self, offer_id, delivery_included=0, fields='STANDARD'):
        """
        Информация о товарном предложении

        :param offer_id: Идентификатор товарного предложения
        :type offer_id: str

        :param delivery_included: Признак включения цены доставки в цену товарного предложения
        :type delivery_included: bool

        :param fields: Параметры предложений, которые необходимо показать в выходных данных

            * **ACTIVE_FILTERS** — активные фильтры
            * **CATEGORY** — информация о категории предложения
            * **DELIVERY** — информация о доставке
            * **DISCOUNT** — скидка
            * **OFFERS_LINK** — Ссылка на страницу с офферами для той же модели в том же магазине
            * **OUTLET** — информация о точке выдачи производетеля
            * **OUTLET_COUNT** — Количество точек выдачи предложени
            * **PHOTO** — фото предложения
            * **SHOP** — магазин от которого поступило предложенение
            * **SHOP_ORGANIZATION** — юридическая информация: юридический и фактический адрес, ОГРН, тип организации, ссылка на реквизиты
            * **SHOP_RATING** — рейтинг магазина
            * **VENDOR** — информация о поставщике
            * **ALL** = Все значения
            * **SHOP_ALL** = SHOP_ORGANIZATION, SHOP_RATING
            * **STANDARD** = CATEGORY, DELIVERY, OUTLET, OUTLET_COUNT, PHOTO, SHOP, SHOP_RATING

        :type fields: str or list[str]

        :raises DeliveryIncludedParamError: недопустимое значение параметра delivery_included
        :raises FieldsParamError: недопустимое значение параметра fields

        :return: Информация об указанном товарном предложении
        :rtype: response.Offer

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/offers-controller-v2-get-offer-docpage/
        """
        params = {}

        if delivery_included:
            if str(delivery_included).upper() in [0, '0', 'F', 'FALSE', 'N', 'NO']:
                delivery_included = 'FALSE'
            elif str(delivery_included).upper() in [1, '1', 'T', 'TRUE', 'Y', 'YES']:
                delivery_included = 'TRUE'
            else:
                raise DeliveryIncludedParamError('"delivery_included" param is wrong')
            params['delivery_included'] = delivery_included

        if fields:
            params['fields'] = self._validate_fields(fields, constants.OFFER_FIELDS)

        return Offer(self._request('offers/{}', offer_id, params))

    def model_opinions(self, model_id, grade=None, max_comments=0, count=10, page=1, how=None, sort='DATE'):
        """
        Отзывы о модели

        :param model_id: Идентификатор модели
        :type model_id: int or str

        :param grade: Оценка, выставленная автором отзыва
        :type grade: int

        :param max_comments: Максимальное количество комментариев, возвращаемых для каждого отзыва
        :type max_comments: int

        :param count: IP-адрес пользователя
        :type count: int

        :param page: Номер страницы
        :type page: int

        :param how: Направление сортировки
        :type how: str

        :param sort: Тип сортировки отзывов
        :type sort: str

        :raises GradeParamError: недопустимое значение параметра grade
        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page
        :raises HowParamError: недопустимое значение параметра how
        :raises SortParamError: недопустимое значение параметра sort

        :return: Отзывы пользователей о модели
        :rtype: response.ModelOpinions

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/opinions-controller-v2-get-model-opinions-docpage/
        """
        params = {}

        if grade < 1 or grade > 5:
            raise GradeParamError('"grade" param must be between 1 and 5')

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        if max_comments:
            params['max_comments'] = max_comments

        if how:
            if how not in ['ASC', 'DESC']:
                raise HowParamError('"how" param is wrong')
            params['how'] = how

        if sort:
            if sort not in ('DATE', 'GRADE', 'RANK'):
                raise SortParamError('"sort" param is wrong')
            params['sort'] = sort
        return ModelOpinions(self._request('models/{}/opinions', model_id, params))

    def shop_opinions(self, shop_id, grade=None, max_comments=0, count=10, page=1, how=None, sort='DATE'):
        """
        Отзывы о магазине

        :param shop_id: Идентификатор магазина
        :type shop_id: int

        :param grade: Оценка, выставленная автором отзыва
        :type grade: int

        :param max_comments: Максимальное количество комментариев, возвращаемых для каждого отзыва
        :type max_comments: int

        :param count: IP-адрес пользователя
        :type count: int

        :param page: Номер страницы
        :type page: int

        :param how: Направление сортировки
        :type how: str

        :param sort: Тип сортировки отзывов
        :type sort: str

        :raises GradeParamError: недопустимое значение параметра grade
        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page
        :raises HowParamError: недопустимое значение параметра how
        :raises SortParamError: недопустимое значение параметра sort

        :return: Отзывы пользователей о магазине
        :rtype: response.ShopOpinions

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/opinions-controller-v2-get-shop-opinions-docpage/
        """
        params = {}

        if grade:
            if grade < 1 or grade > 5:
                raise GradeParamError('"grade" param must be between 1 and 5')
            params['grade'] = grade

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        if max_comments:
            params['max_comments'] = max_comments

        if how:
            if how not in ['ASC', 'DESC']:
                raise HowParamError('"how" param is wrong')
            params['how'] = how

        if sort:
            if sort not in ('DATE', 'GRADE', 'RANK'):
                raise SortParamError('"sort" param is wrong')
            params['sort'] = sort

        return ShopOpinions(self._request('shops/{}/opinions', shop_id, params))

    def shop(self, shop_id, fields=None):
        """
        Информация о магазине

        :param shop_id: Идентификатор магазина
        :type shop_id: int

        :param fields: Свойства магазинов, которые необходимо показать в выходных данных

        * **DATE** — сортировка по дате написания отзыва
        * **GRADE** — сортировка по оценке пользователем модели
        * **RANK** — сортировка по полезности отзыва

        :type fields: str or list[str]

        :raises FieldsParamError: недопустимое значение параметра fields

        :return: Информация об указанном магазине
        :rtype: response.Shop

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/shops-controller-v2-get-shop-docpage/
        """
        params = {}

        if fields:
            params['fields'] = self._validate_fields(fields, constants.SHOP_FIELDS)

        return Shop(self._request('shops/{}', shop_id, params))

    def shops(self, host, fields=None, geo_id=None):
        """
        Поиск магазина по хосту или URL

        :param host: Хост или URL магазина, который требуется найти
        :type host: str

        :param fields: Свойства магазинов, которые необходимо показать в выходных данных

            * **DATE** — сортировка по дате написания отзыва
            * **GRADE** — сортировка по оценке пользователем модели
            * **RANK** — сортировка по полезности отзыва

        :type fields: str or list[str]

        :param geo_id: Идентификатор региона
        :type geo_id: int or str

        :raises NoGeoIdOrIP: недопустимое значение параметра geo_id
        :raises FieldsParamError: недопустимое значение параметра fields

        :return: Информация о найденном магазине по указанному в запросе хосту или URL
        :rtype: response.Shops

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/shops-controller-v2-get-shop-list-docpage/
        """
        params = {'host': host}

        if geo_id is None:
            raise NoGeoIdOrIP(
                "You must provide geo_id")
        else:
            params['geo_id'] = geo_id

        if fields:
            params['fields'] = self._validate_fields(fields, constants.SHOP_FIELDS)

        return Shops(self._request('shops', None, params))

    def geo_regions_shops_summary(self, region_id, fields='DELIVERY_COUNT,HOME_COUNT'):
        """
        Количество магазинов, работающих в регионе

        :param region_id: Идентификатор региона
        :type region_id: int

        :param fields: Параметры, которые необходимо показать в выдаче
        :type fields: str or list[str]

        :raises FieldsParamError: недопустимое значение параметра fields

        :return: Информация о количестве магазинов и типах их работы в указанном регионе
        :rtype: response.ShopsSummary

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/shops-controller-v2-get-shop-summary-docpage/
        """
        params = {}

        if fields:
            params['fields'] = self._validate_fields(fields,
                                                     ('DELIVERY_COUNT', 'HOME_COUNT',
                                                      'TOTAL_COUNT', 'ALL'))

        return ShopsSummary(self._request('geo/regions/{}/shops/summary', region_id, params))

    def model_outlets(self, model_id, boundary=None, fields='STANDARD', type='PICKUP,STORE', filters=None, count=10,
                      page=1, how=None, sort='RELEVANCY', latitude=None, longitude=None):
        """
        Список пунктов выдачи модели

        :param model_id: Идентификатор модели
        :type model_id: int or str

        :param boundary: Координаты квадрата на местности для выдачи точек продаж на карте.
        :type boundary: str

        :param fields: Поля точек продажи, которые попадут в выдачу

            * **OFFER** — Информация о товарнном предложении, соответствующем точке продажи
            * **OFFER_ACTIVE_FILTERS** — активные фильтры.
            * **OFFER_CATEGORY** — информация о категории предложения.
            * **OFFER_DELIVERY** — информация о доставке.
            * **OFFER_DISCOUNT** — скидка.
            * **OFFER_OFFERS_LINK** — Ссылка на страницу с офферами для той же модели в том же магазине.
            * **OFFER_OUTLET** — информация о точке выдачи производетеля.
            * **OFFER_OUTLET_COUNT** — Количество точек выдачи предложения
            * **OFFER_PHOTO** — фото предложения.
            * **OFFER_SHOP** — магазин от которого поступило предложенение.
            * **OFFER_VENDOR** — информация о поставщике.
            * **SHOP** — Информация о магазине, сортировка по полезности отзыва
            * **SHOP_ORGANIZATION** — юридическая информация: юридический и фактический адрес, ОГРН, тип организации, ссылка на реквизиты.
            * **SHOP_RATING** — рейтинг магазина.
            * **ALL** = Все значения
            * **OFFER_ALL** = OFFER_ACTIVE_FILTERS, OFFER_BUNDLE_SETTINGS, OFFER_CATEGORY, OFFER_DELIVERY, OFFER_DISCOUNT, OFFER_LINK, OFFER_OFFERS_LINK, OFFER_OUTLET, OFFER_OUTLET_COUNT, OFFER_PHOTO, OFFER_SHOP, OFFER_VENDOR
            * **SHOP_ALL** = SHOP_ORGANIZATION, SHOP_RATING
            * **STANDARD** = OFFER_CATEGORY, OFFER_DELIVERY, OFFER_OUTLET, OFFER_OUTLET_COUNT, OFFER_PHOTO, OFFER_SHOP, SHOP_RATING

        :type fields: str or list[str]

        :param type: Типы пунктов выдачи товара
        :type type: str or list[str]

        :param filters: Параметры задают условия фильтрации моделей и предложений на модель
        :type filters: dict

        :param count: Размер страницы (количество элементов на странице)
        :type count: int

        :param page: Номер страницы
        :type page: int

        :param how: Направление сортировки
        :type how: str

        :param sort: Тип сортировки товарных предложений

            * **DATE** — сортировка по дате
            * **DELIVERY_TIME** — сортировка по времени доставки
            * **DISCOUNT** — сортировка по размеру скидки
            * **DISTANCE** — сортировка по расстоянию до ближайшей точки продаж (значение доступно только при указании местоположения пользователя)
            * **NOFFERS** — сортировка по количеству предложений
            * **OPINIONS** — сортировка по количеству отзывов
            * **POPULARITY** — сортировка по популярности
            * **PRICE** — сортировка по цене
            * **QUALITY** — сортировка по рейтингу
            * **RATING** — сортировка по рейтингу
            * **RELEVANCY** — сортировка по релевантности

        :type sort: str

        :param latitude: Широта
        :type latitude: float

        :param longitude: Долгота
        :type longitude: float

        :raises FieldsParamError: недопустимое значение параметра fields
        :raises TypeParamError: недопустимое значение параметра type
        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page
        :raises HowParamError: недопустимое значение параметра how
        :raises SortParamError: недопустимое значение параметра sort
        :raises GeoParamError: недопустимое значение параметра latitude
        :raises GeoParamError: недопустимое значение параметра longitude

        :return: Список пунктов выдачи/точек продаж, в которых представлена указанная модель
        :rtype: response.Outlets

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/outlet-controller-v2-get-model-outlets-docpage/
        """
        params = {}

        # ToDO нужно добавить преобразование типа в эталонный
        if boundary:
            params['boundary'] = boundary

        if fields:
            params['fields'] = self._validate_fields(fields, constants.OUTLETS_FIELDS)

        if type:
            for field in type.split(','):
                if field not in (
                        'PICKUP', 'STORE',
                        'ALL'):
                    raise TypeParamError('"type" param is wrong')
            params['type'] = type

        if filters:
            for (k, v) in filters.items():
                params[k] = v

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        if how:
            if how not in ('ASC', 'DESC'):
                raise HowParamError('"how" param is wrong')

        if sort:
            if sort not in constants.MODEL_SORT:
                raise SortParamError('"sort" param is wrong')
            params['sort'] = sort

        # Todo Ограничение. Для sort=DISCOUNT возможна только сортировка по убыванию (how=DESC).

        # todo Ограничение. Оба парметра должны быть определены совместно. Не допускается указывать один без другого.

        if latitude:
            if latitude < -90 or latitude > 90:
                raise GeoParamError('"latitude" param must be between -90 and 90')
            params['latitude'] = latitude

        if longitude:
            if longitude < -180 or longitude > 180:
                raise GeoParamError('"longitude" param must be between -180 and 180')
            params['longitude'] = longitude

        return Outlets(self._request('models/{}/outlets', model_id, params))

    def shop_outlets(self, shop_id, boundary=None, fields='STANDARD', type='PICKUP,STORE', filters=None, count=10,
                     page=1, how=None, sort='RELEVANCY', latitude=None, longitude=None):
        """
        Пункты выдачи товаров магазина

        :param shop_id: Идентификатор магазина
        :type shop_id: int

        :param boundary: Координаты квадрата на местности для выдачи точек продаж на карте.
        :type boundary: str

        :param fields: Поля точек продажи, которые попадут в выдачу
        :type fields: str or list[str]

        :param type: Типы пунктов выдачи товара
        :type type: str or list[str]

        :param filters: Параметры задают условия фильтрации моделей и предложений на модель
        :type filters: dict

        :param count: Размер страницы (количество элементов на странице)
        :type count: int

        :param page: Номер страницы
        :type page: int

        :param how: Направление сортировки
        :type how: str

        :param sort: Тип сортировки товарных предложений

            * **DATE** — сортировка по дате
            * **DELIVERY_TIME** — сортировка по времени доставки
            * **DISCOUNT** — сортировка по размеру скидки
            * **DISTANCE** — сортировка по расстоянию до ближайшей точки продаж (значение доступно только при указании местоположения пользователя)
            * **NOFFERS** — сортировка по количеству предложений
            * **OPINIONS** — сортировка по количеству отзывов
            * **POPULARITY** — сортировка по популярности
            * **PRICE** — сортировка по цене
            * **QUALITY** — сортировка по рейтингу
            * **RATING** — сортировка по рейтингу
            * **RELEVANCY** — сортировка по релевантности

        :type sort: str

        :param latitude: Широта
        :type latitude: float

        :param longitude: Долгота
        :type longitude: float

        :raises FieldsParamError: недопустимое значение параметра fields
        :raises TypeParamError: недопустимое значение параметра type
        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page
        :raises HowParamError: недопустимое значение параметра how
        :raises SortParamError: недопустимое значение параметра sort
        :raises GeoParamError: недопустимое значение параметра latitude
        :raises GeoParamError: недопустимое значение параметра longitude

        :return: Cписок пунктов выдачи/точек продаж магазина
        :rtype: response.Outlets

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/shops-controller-v2-get-shop-outlets-docpage/
        """
        params = {}

        # ToDO нужно добавить преобразование типа в эталонный
        if boundary:
            params['boundary'] = boundary

        if fields:
            params['fields'] = self._validate_fields(fields, constants.OUTLETS_FIELDS)

        if type:
            for field in type.split(','):
                if field not in (
                        'PICKUP', 'STORE',
                        'ALL'):
                    raise TypeParamError('"fields" param is wrong')
            params['type'] = type

        if filters:
            for (k, v) in filters.items():
                params[k] = v

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        if how:
            if how not in ('ASC', 'DESC'):
                raise HowParamError('"how" param is wrong')
            params['how'] = how

        if sort:
            if sort not in constants.MODEL_SORT:
                raise SortParamError('"sort" param is wrong')
            params['sort'] = sort

        # Todo Ограничение. Для sort=DISCOUNT возможна только сортировка по убыванию (how=DESC).

        # todo Ограничение. Оба парметра должны быть определены совместно. Не допускается указывать один без другого.

        if latitude:
            if latitude < -90 or latitude > 90:
                raise GeoParamError('"latitude" param must be between -90 and 90')
            params['latitude'] = latitude

        if longitude:
            if longitude < -180 or longitude > 180:
                raise GeoParamError('"longitude" param must be between -180 and 180')
            params['longitude'] = longitude

        return Outlets(self._request('shops/{}/outlets', shop_id, params))

    def offer_outlets(self, offer_id, boundary=None, fields='STANDARD', type='PICKUP,STORE', filters=None, count=10,
                      page=1, how=None, sort='RELEVANCY', latitude=None, longitude=None):
        """
        Список пунктов выдачи товарного предложения

        :param offer_id: Идентификатор товарного предложения
        :type offer_id: int

        :param boundary: Координаты квадрата на местности для выдачи точек продаж на карте.
        :type boundary: str

        :param fields: Поля точек продажи, которые попадут в выдачу

            * **OFFER** — Информация о товарнном предложении, соответствующем точке продажи
            * **OFFER_ACTIVE_FILTERS** — активные фильтры.
            * **OFFER_CATEGORY** — информация о категории предложения.
            * **OFFER_DELIVERY** — информация о доставке.
            * **OFFER_DISCOUNT** — скидка.
            * **OFFER_OFFERS_LINK** — Ссылка на страницу с офферами для той же модели в том же магазине.
            * **OFFER_OUTLET** — информация о точке выдачи производетеля.
            * **OFFER_OUTLET_COUNT** — Количество точек выдачи предложения
            * **OFFER_PHOTO** — фото предложения.
            * **OFFER_SHOP** — магазин от которого поступило предложенение.
            * **OFFER_VENDOR** — информация о поставщике.
            * **SHOP** — Информация о магазине, сортировка по полезности отзыва
            * **SHOP_ORGANIZATION** — юридическая информация: юридический и фактический адрес, ОГРН, тип организации, ссылка на реквизиты.
            * **SHOP_RATING** — рейтинг магазина.
            * **ALL** = Все значения
            * **OFFER_ALL** = OFFER_ACTIVE_FILTERS, OFFER_BUNDLE_SETTINGS, OFFER_CATEGORY, OFFER_DELIVERY, OFFER_DISCOUNT, OFFER_LINK, OFFER_OFFERS_LINK, OFFER_OUTLET, OFFER_OUTLET_COUNT, OFFER_PHOTO, OFFER_SHOP, OFFER_VENDOR
            * **SHOP_ALL** = SHOP_ORGANIZATION, SHOP_RATING
            * **STANDARD** = OFFER_CATEGORY, OFFER_DELIVERY, OFFER_OUTLET, OFFER_OUTLET_COUNT, OFFER_PHOTO, OFFER_SHOP, SHOP_RATING

        :type fields: str or list[str]

        :param type: Типы пунктов выдачи товара
        :type type: str or list[str]

        :param filters: Параметры задают условия фильтрации моделей и предложений на модель
        :type filters: dict

        :param count: Размер страницы (количество элементов на странице)
        :type count: int

        :param page: Номер страницы
        :type page: int

        :param how: Направление сортировки
        :type how: str

        :param sort: Тип сортировки товарных предложений

            * **DATE** — сортировка по дате
            * **DELIVERY_TIME** — сортировка по времени доставки
            * **DISCOUNT** — сортировка по размеру скидки
            * **DISTANCE** — сортировка по расстоянию до ближайшей точки продаж (значение доступно только при указании местоположения пользователя)
            * **NOFFERS** — сортировка по количеству предложений
            * **OPINIONS** — сортировка по количеству отзывов
            * **POPULARITY** — сортировка по популярности
            * **PRICE** — сортировка по цене
            * **QUALITY** — сортировка по рейтингу
            * **RATING** — сортировка по рейтингу
            * **RELEVANCY** — сортировка по релевантности

        :type sort: str

        :param latitude: Широта
        :type latitude: float

        :param longitude: Долгота
        :type longitude: float

        :raises FieldsParamError: недопустимое значение параметра fields
        :raises TypeParamError: недопустимое значение параметра type
        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page
        :raises HowParamError: недопустимое значение параметра how
        :raises SortParamError: недопустимое значение параметра sort
        :raises GeoParamError: недопустимое значение параметра latitude
        :raises GeoParamError: недопустимое значение параметра longitude

        :return: Список пунктов выдачи/точек продаж указанного товарного предложения
        :rtype: response.Outlets

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/outlet-controller-v2-get-offer-outlets-docpage/
        """
        params = {}

        # ToDO нужно добавить преобразование типа в эталонный
        if boundary:
            params['boundary'] = boundary

        if fields:
            params['fields'] = self._validate_fields(fields, constants.OUTLETS_FIELDS)

        if type:
            for field in type.split(','):
                if field not in (
                        'PICKUP', 'STORE',
                        'ALL'):
                    raise TypeParamError('"fields" param is wrong')
            params['type'] = type

        if filters:
            for (k, v) in filters.items():
                params[k] = v

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        if how:
            if how not in ('ASC', 'DESC'):
                raise HowParamError('"how" param is wrong')
            params['how'] = how

        if sort:
            if sort not in constants.MODEL_SORT:
                raise SortParamError('"sort" param is wrong')
            params['sort'] = sort

        # Todo Ограничение. Для sort=DISCOUNT возможна только сортировка по убыванию (how=DESC).

        # todo Ограничение. Оба парметра должны быть определены совместно. Не допускается указывать один без другого.

        if latitude:
            if latitude < -90 or latitude > 90:
                raise GeoParamError('"latitude" param must be between -90 and 90')
            params['latitude'] = latitude

        if longitude:
            if longitude < -180 or longitude > 180:
                raise GeoParamError('"longitude" param must be between -180 and 180')
            params['longitude'] = longitude

        return Outlets(self._request('offers/{}/outlets', offer_id, params))

    def geo_regions(self, fields=None, count=10, page=1):
        """
        Список регионов

        :param fields: Параметры региона, которые необходимо включить в выдачу

            * **DECLENSIONS** — Название региона в разных падежах
            * **PARENT** — Родительский регион
            * **ALL** = Все значения

        :type fields: str or list[str]

        :param count: Размер страницы (количество элементов на странице)
        :type count: int

        :param page: Номер страницы
        :type page: int

        :raises FieldsParamError: недопустимое значение параметра fields
        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page

        :return: Список регионов
        :rtype: response.Regions

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/geo-controller-v2-get-region-root-docpage/
        """
        params = {}

        if fields:
            params['fields'] = self._validate_fields(fields, constants.GEO_FIELDS)

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        return Regions(self._request('geo/regions', None, params))

    def geo_regions_children(self, region_id, fields=None, count=10, page=1):
        """
        Список дочерних регионов

        :param region_id: Идентификатор региона
        :type region_id: int

        :param fields: Параметры региона, которые необходимо включить в выдачу

            * **DECLENSIONS** — Название региона в разных падежах
            * **PARENT** — Родительский регион
            * **ALL** = Все значения

        :type fields: str or list[str]

        :param count: Размер страницы (количество элементов на странице)
        :type count: int

        :param page: Номер страницы
        :type page: int

        :raises FieldsParamError: недопустимое значение параметра fields
        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page

        :return: Список регионов
        :rtype: response.Regions

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/geo-controller-v2-get-children-docpage/
        """
        params = {}

        if fields:
            params['fields'] = self._validate_fields(fields, constants.GEO_FIELDS)

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        return Regions(self._request('geo/regions/{}/children', region_id, params))

    def geo_region(self, region_id, fields=None):
        """
        Информация о регионе

        :param region_id: Идентификатор региона
        :type region_id: int

        :param fields: Параметры региона, которые необходимо включить в выдачу

            * **DECLENSIONS** — Название региона в разных падежах
            * **PARENT** — Родительский регион
            * **ALL** = Все значения

        :type fields: str or list[str]

        :raises FieldsParamError: недопустимое значение параметра fields

        :return: Информация о регионе
        :rtype: response.Region

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/geo-controller-v2-get-region-docpage/
        """
        params = {}

        if fields:
            params['fields'] = self._validate_fields(fields, constants.GEO_FIELDS)

        return Region(self._request('geo/regions/{}', region_id, params))

    def geo_suggest(self, fields=None,
                    types='CITY, CITY_DISTRICT, REGION, RURAL_SETTLEMENT, SECONDARY_DISTRICT, VILLAGE',
                    count=10, page=1):
        """
        Текстовый поиск региона

        :param fields: Параметры региона, которые необходимо включить в выдачу

            * **DECLENSIONS** — Название региона в разных падежах
            * **PARENT** — Родительский регион
            * **ALL** = Все значения

        :type fields: str or list[str]

        :param types: Тип региона
        :type types: str or list[str]

        :param count: Размер страницы (количество элементов на странице)
        :type count: int

        :param page: Номер страницы
        :type page: int

        :raises FieldsParamError: недопустимое значение параметра fields
        :raises TypeParamError: недопустимое значение параметра type
        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page

        :return: Список регионов, подходящих под заданные условия поиска
        :rtype: response.Suggests

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/geo-controller-v2-suggest-docpage/
        """
        params = {}

        if fields:
            params['fields'] = self._validate_fields(fields, constants.GEO_FIELDS)

        if types:
            for field in types.split(','):
                if field not in (
                        'AIRPORT', 'CITY', 'CITY_DISTRICT', 'CONTINENT', 'COUNTRY', 'COUNTRY_DISTRICT', 'METRO_STATION',
                        'MONORAIL_STATION', 'OVERSEAS_TERRITORY', 'REGION', 'RURAL_SETTLEMENT', 'SECONDARY_DISTRICT',
                        'SUBJECT_FEDERATION', 'SUBJECT_FEDERATION_DISTRICT', 'VILLAGE', 'ALL'):
                    raise TypeParamError('"type" param is wrong')
            params['types'] = types

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        return Suggests(self._request('geo/suggest', None, params))

    def vendors(self, fields=None, count=10, page=1):
        """
        Список производителей

        :param fields: Параметры региона, которые необходимо включить в выдачу

            * **CATEGORIES** — Описание категорий, в которых представлен данный производитель
            * **CATEGORY_PARENT** — информация о родительской категории.
            * **CATEGORY_STATISTICS** — статистика по категории. Например, количество моделей и товарных предложений в категории.
            * **CATEGORY_WARNINGS** — предупреждения, связанные с показом категории.
            * **TOP_CATEGORIES** — Список наиболее популярных категорий товаров производителя
            * **ALL** = Все значения
            * **CATEGORY_ALL** = CATEGORY_LINK, CATEGORY_PARENT, CATEGORY_STATISTICS, CATEGORY_WARNINGS

        :type fields: str or list[str]

        :param count: Размер страницы (количество элементов на странице)
        :type count: int

        :param page: Номер страницы
        :type page: int

        :raises FieldsParamError: недопустимое значение параметра fields
        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page

        :return: Cписок производителей, товары которых размещаются на Яндекс.Маркете
        :rtype: response.Vendors

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/vendor-controller-v2-get-vendor-list-docpage/
        """
        params = {}

        if fields:
            params['fields'] = self._validate_fields(fields, constants.VENDOR_FIELDS)

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        return Vendors(self._request('vendors', None, params))

    def vendor(self, vendor_id, fields=None):
        """
        Информация о производителе

        :param vendor_id: Идентификатор производителя
        :type vendor_id: int

        :param fields: Свойства производителя, которые необходимо показать в выходных данных

            * **CATEGORIES** — Описание категорий, в которых представлен данный производитель
            * **CATEGORY_PARENT** — информация о родительской категории.
            * **CATEGORY_STATISTICS** — статистика по категории. Например, количество моделей и товарных предложений в категории.
            * **CATEGORY_WARNINGS** — предупреждения, связанные с показом категории.
            * **TOP_CATEGORIES** — Список наиболее популярных категорий товаров производителя
            * **ALL** = Все значения
            * **CATEGORY_ALL** = CATEGORY_LINK, CATEGORY_PARENT, CATEGORY_STATISTICS, CATEGORY_WARNINGS

        :type fields: str or list[str]

        :raises FieldsParamError: недопустимое значение параметра fields

        :return: Информация об указанном производителе
        :rtype: response.Vendor

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/vendor-controller-v2-get-vendor-docpage/
        """
        params = {}

        if fields:
            params['fields'] = self._validate_fields(fields, constants.VENDOR_FIELDS)

        return Vendor(self._request('vendors/{}', vendor_id, params))

    def vendors_match(self, name, fields=None):
        """
        Подбор производителя по названию

        :param name: Название производителя
        :type name: str

        :param fields: Свойства производителя, которые необходимо показать в выходных данных

            * **CATEGORIES** — Описание категорий, в которых представлен данный производитель
            * **CATEGORY_PARENT** — информация о родительской категории.
            * **CATEGORY_STATISTICS** — статистика по категории. Например, количество моделей и товарных предложений в категории.
            * **CATEGORY_WARNINGS** — предупреждения, связанные с показом категории.
            * **TOP_CATEGORIES** — Список наиболее популярных категорий товаров производителя
            * **ALL** = Все значения
            * **CATEGORY_ALL** = CATEGORY_LINK, CATEGORY_PARENT, CATEGORY_STATISTICS, CATEGORY_WARNINGS

        :type fields: str or list[str]

        :raises FieldsParamError: недопустимое значение параметра fields

        :return: Производитель, наиболее подходящего под заданное во входных данных название
        :rtype: response.Vendor

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/vendor-controller-v2-match-vendor-docpage/
        """
        params = {'name': name}

        if fields:
            # todo добавить всюду CATEGORY_ALL
            params['fields'] = self._validate_fields(fields, constants.VENDOR_FIELDS)

        return Vendor(self._request('vendors/match', None, params))

    def search(self, text, delivery_included=False, fields=None, onstock=0, outlet_types=None, price_max=None,
               price_min=None, result_type='ALL', shop_id=None, warranty=0, filters=None, barcode=False,
               search_type=None,
               category_id=None, hid=None, count=10, page=1, how=None, sort=None, latitude=None, longitude=None,
               geo_id=None, remote_ip=None):
        """
        Текстовый поиск

        :param text: Текст запроса
        :type text: str

        :param delivery_included: Признак включения цены доставки в цену товарного предложения
        :type delivery_included: str or int or bool

        :param fields: Праметры модели/товарного предложения, которые необходимо показать в выходных данных.
        :type fields: str or list[str]

        :param onstock: Признак в наличии
        :type onstock: str or int or bool

        :param outlet_types: Типы точек продажи
        :type outlet_types: str or list[str]

        :param price_max: Максимальная цена
        :type price_max: int

        :param price_min: Минимальная цена
        :type price_min: int

        :param result_type: Возможные значения
        :type result_type: str

        :param shop_id: Идентификаторы магазинов
        :type shop_id: str or list[str]

        :param warranty: Признак "Гарантия производителя"
        :type warranty: str or int or bool

        :param filters: Параметры задают условия фильтрации моделей и предложений на модель
        :type filters: dict

        :param barcode: Признак поиска по штрихкоду
        :type barcode: bool

        :param search_type: Тип поискового запроса
        :type search_type: str

        :param category_id: Идентификаторы категорий
        :type category_id: int or str

        :param hid: Идентификаторы категорий
        :type hid: int

        :param count: Размер страницы (количество элементов на странице)
        :type count: int

        :param page: Номер страницы
        :type page: int

        :param how: Направление сортировки
        :type how: str

        :param sort: Тип сортировки товарных предложений

            * **DATE** — сортировка по дате
            * **DELIVERY_TIME** — сортировка по времени доставки
            * **DISCOUNT** — сортировка по размеру скидки
            * **DISTANCE** — сортировка по расстоянию до ближайшей точки продаж (значение доступно только при указании местоположения пользователя)
            * **NOFFERS** — сортировка по количеству предложений
            * **OPINIONS** — сортировка по количеству отзывов
            * **POPULARITY** — сортировка по популярности
            * **PRICE** — сортировка по цене
            * **QUALITY** — сортировка по рейтингу
            * **RATING** — сортировка по рейтингу
            * **RELEVANCY** — сортировка по релевантности

        :type sort: str

        :param latitude: Широта
        :type latitude: float

        :param longitude: Долгота
        :type longitude: float

        :param geo_id: Идентификатор региона
        :type geo_id: int or str

        :param remote_ip: Идентификатор региона пользователя
        :type remote_ip: str

        :raises NoGeoIdOrIP: не передан обязательный параметр geo_id или remote_ip
        :raises DeliveryIncludedParamError: недопустимое значение параметра delivery_included
        :raises FieldsParamError: недопустимое значение параметра fields
        :raises OnstockParamError: недопустимое значение параметра onstock
        :raises OutletTypesParamError: недопустимое значение параметра outlet_types
        :raises ResultTypeParamError: недопустимое значение параметра result_type
        :raises WarrantyParamError: недопустимое значение параметра warranty
        :raises SearchTypeParamError: недопустимое значение параметра search_type
        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page
        :raises HowParamError: недопустимое значение параметра how
        :raises SortParamError: недопустимое значение параметра sort
        :raises GeoParamError: недопустимое значение параметра latitude
        :raises GeoParamError: недопустимое значение параметра longitude

        :return: Список моделей и товарных предложений, удовлетворяющих заданным в запросе условиям поиска
        :rtype: response.Search

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/search-controller-v2-search-docpage/
        """
        params = {'text': text}

        if geo_id is None and remote_ip is None:
            raise NoGeoIdOrIP(
                "You must provide either geo_id or remote_ip")

        if geo_id:
            params['geo_id'] = geo_id

        if remote_ip:
            params['remote_ip'] = remote_ip

        if delivery_included:
            if str(delivery_included).upper() in [0, '0', 'F', 'FALSE', 'N', 'NO']:
                delivery_included = 'FALSE'
            elif str(delivery_included).upper() in [1, '1', 'T', 'TRUE', 'Y', 'YES']:
                delivery_included = 'TRUE'
            else:
                raise DeliveryIncludedParamError('"delivery_included" param is wrong')
            params['delivery_included'] = delivery_included

        if fields:
            params['fields'] = self._validate_fields(fields,
                                                     ('FILTERS', 'FOUND_CATEGORIES',

                                                      'MODEL_CATEGORY', 'MODEL_DEFAULT_OFFER', 'MODEL_DISCOUNTS',
                                                      'MODEL_FACTS', 'MODEL_FILTER_COLOR', 'MODEL_MEDIA',
                                                      'MODEL_NAVIGATION_NODE',
                                                      'MODEL_OFFERS', 'MODEL_PHOTO', 'MODEL_PHOTOS',
                                                      'MODEL_PRICE', 'MODEL_RATING', 'MODEL_SPECIFICATION',
                                                      'MODEL_VENDOR', 'OFFER_ACTIVE_FILTERS', 'OFFER_CATEGORY',
                                                      'OFFER_DELIVERY', 'OFFER_DISCOUNT',
                                                      'OFFER_OFFERS_LINK', 'OFFER_OUTLET', 'OFFER_OUTLET_COUNT',
                                                      'OFFER_PHOTO',
                                                      'OFFER_PHOTO', 'OFFER_VENDOR', 'SHOP_ORGANIZATION', 'SHOP_RATING',
                                                      'SORTS', 'ALL', 'MODEL_ALL',
                                                      'OFFER_ALL', 'SHOP_ALL', 'STANDARD'))

        if onstock:
            if str(onstock).upper() in [0, '0', 'F', 'FALSE', 'N', 'NO']:
                onstock = 'FALSE'
            elif str(onstock).upper() in [1, '1', 'T', 'TRUE', 'Y', 'YES']:
                onstock = 'TRUE'
            else:
                raise OnstockParamError('"onstock" param is wrong')
            params['onstock'] = onstock

        if outlet_types:
            for field in outlet_types.split(','):
                if field not in (
                        'DELIVERY', 'PICKUP', 'STORE', 'ALL'):
                    raise OutletTypesParamError('"outlet_types" param is wrong')
            params['outlet_types'] = outlet_types

        if price_max:
            params['price_max'] = price_max

        if price_min:
            params['price_min'] = price_min

        if result_type:
            if result_type not in (
                    'ALL', 'MODELS', 'OFFERS'):
                raise ResultTypeParamError('"result_type" param is wrong')
            params['fields'] = fields

        if shop_id:
            params['shop_id'] = shop_id

        if warranty:
            if str(warranty).upper() in [0, '0', 'F', 'FALSE', 'N', 'NO']:
                warranty = 'FALSE'
            elif str(warranty).upper() in [1, '1', 'T', 'TRUE', 'Y', 'YES']:
                warranty = 'TRUE'
            else:
                raise WarrantyParamError('"warranty" param is wrong')
            params['warranty'] = warranty

        if filters:
            for (k, v) in filters.items():
                params[k] = v

        if barcode:
            params['barcode'] = barcode
            # todo Параметр действует только, если не указан search_type

        if search_type:
            if search_type not in (
                    'BARCODE', 'ISBN', 'TEXT'):
                raise SearchTypeParamError('"search_type" param is wrong')
            params['search_type'] = search_type

        if category_id:
            params['category_id'] = category_id

        if hid:
            params['hid'] = hid

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        if how:
            if how not in ('ASC', 'DESC'):
                raise HowParamError('"how" param is wrong')
            params['how'] = how

        if sort:
            if sort not in constants.MODEL_SORT:
                raise SortParamError('"sort" param is wrong')
            params['sort'] = sort
        # Todo Ограничение. Для sort=DISCOUNT возможна только сортировка по убыванию (how=DESC).

        # todo Ограничение. Оба парметра должны быть определены совместно. Не допускается указывать один без другого.

        if latitude:
            if latitude < -90 or latitude > 90:
                raise GeoParamError('"latitude" param must be between -90 and 90')
            params['latitude'] = latitude

        if longitude:
            if longitude < -180 or longitude > 180:
                raise GeoParamError('"longitude" param must be between -180 and 180')
            params['longitude'] = longitude

        return Search(self._request('search', None, params))

    def categories_search(self, category_id, geo_id=None, remote_ip=None, fields=None, result_type='ALL', rs=None,
                          shop_regions=None, filters=None,
                          count=10, page=1, how=None, sort=None):
        """
        Подбор по параметрам в категории

        :param category_id: Идентификатор категории
        :type category_id: int or str

        :param geo_id: Идентификатор региона
        :type geo_id: int or str

        :param remote_ip: Идентификатор региона пользователя
        :type remote_ip: str

        :param fields: Поля, которые необходимо показать в выходных данных
        :type fields: str or list[str]

        :param result_type: Тип возвращаемых данных
        :type result_type: str

        :param rs: Поле содержащее закодированную информацию о текстовом запросе после редиректа, на которую будет ориентироватся поиск
        :type rs: str

        :param shop_regions: Идентификаторы регионов магазинов
        :type shop_regions: str or list[str]

        :param filters: Параметры задают условия фильтрации моделей и предложений на модель
        :type filters: dict

        :param count: Размер страницы (количество элементов на странице)
        :type count: int

        :param page: Номер страницы
        :type page: int

        :param how: Направление сортировки
        :type how: str

        :param sort: Тип сортировки товарных предложений
        :type sort: str

        :raises NoGeoIdOrIP: не передан обязательный параметр geo_id или remote_ip
        :raises FieldsParamError: недопустимое значение параметра fields
        :raises ResultTypeParamError: недопустимое значение параметра result_type
        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page
        :raises HowParamError: недопустимое значение параметра how
        :raises SortParamError: недопустимое значение параметра sort

        :return: Список моделей категории и предложений на модели, удовлетворяющих заданным в запросе параметрам
        :rtype: response.Search

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/search-controller-v2-filter-on-category-docpage/
        """
        params = {}

        if geo_id is None and remote_ip is None:
            raise NoGeoIdOrIP(
                "You must provide either geo_id or remote_ip")

        if geo_id:
            params['geo_id'] = geo_id

        if remote_ip:
            params['remote_ip'] = remote_ip

        if fields:
            params['fields'] = self._validate_fields(fields,
                                                     ('MODEL_CATEGORY', 'MODEL_DEFAULT_OFFER', 'MODEL_DISCOUNTS',
                                                      'MODEL_FACTS', 'MODEL_FILTER_COLOR', 'MODEL_MEDIA',
                                                      'MODEL_NAVIGATION_NODE',
                                                      'MODEL_OFFERS', 'MODEL_PHOTO', 'MODEL_PHOTOS',
                                                      'MODEL_PRICE', 'MODEL_RATING', 'MODEL_SPECIFICATION',
                                                      'MODEL_VENDOR', 'OFFER_ACTIVE_FILTERS', 'OFFER_CATEGORY',
                                                      'OFFER_DELIVERY', 'OFFER_DISCOUNT',
                                                      'OFFER_OFFERS_LINK', 'OFFER_OUTLET', 'OFFER_OUTLET_COUNT',
                                                      'OFFER_PHOTO',
                                                      'OFFER_PHOTO', 'OFFER_VENDOR', 'SHOP_ORGANIZATION', 'SHOP_RATING',
                                                      'ALL', 'MODEL_ALL',
                                                      'OFFER_ALL', 'SHOP_ALL', 'STANDARD'))

        if result_type:
            if result_type not in (
                    'ALL', 'MODELS', 'OFFERS'):
                raise ResultTypeParamError('"result_type" param is wrong')
            params['result_type'] = result_type

        if rs:
            params['rs'] = rs

        if shop_regions:
            params['shop_regions'] = shop_regions

        if filters:
            for (k, v) in filters.items():
                params[k] = v

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        if how:
            if how not in ('ASC', 'DESC'):
                raise HowParamError('"how" param is wrong')
            params['how'] = how

        if sort:
            if sort not in constants.MODEL_SORT:
                raise SortParamError('"sort" param is wrong')
            params['sort'] = sort

        return Search(self._request('categories/{}/search', category_id, params))

    def search_filters(self, text, fields=None):
        """
        Фильтры для поискового запроса

        :param text: Текст запроса
        :type text: str

        :param fields: Поля, которые необходимо показать в выходных данных
        :type fields: str or list[str]

        :raises FieldsParamError: недопустимое значение параметра fields

        :return: Список доступных фильтров и сортировок для укзанного поискового запроса
        :rtype: response.Filters

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/search-controller-v2-get-search-filters-docpage/
        """
        params = {'text': text}

        if fields:
            params['fields'] = self._validate_fields(fields, constants.SEARCH_FILTERS)

        return Filters(self._request('search/filters', None, params))

    def redirect(self, text, redirect_types='SEARCH', barcode=False, search_type=None, category_id=None, hid=None,
                 fields=None, user_agent=None, count=10, page=1, how=None, sort=None, geo_id=None, remote_ip=None):
        """
        Редирект (перенаправление)

        :param text: Текст запроса
        :type text: str

        :param redirect_types: Типы редиректов
        :type redirect_types: str or list[str]

        :param barcode: Признак поиска по штрихкоду
        :type barcode: bool

        :param search_type: Тип поискового запроса
        :type search_type: str

        :param category_id: Идентификаторы категорий
        :type category_id: int

        :param hid: Идентификаторы категорий
        :type hid: int

        :param fields: Праметры модели/товарного предложения, которые необходимо показать в выходных данных.
        :type fields: str or list[str]

        :param user_agent: Признак включения цены доставки в цену товарного предложения
        :type user_agent: str

        :param count: Размер страницы (количество элементов на странице)
        :type count: int

        :param page: Номер страницы
        :type page: int

        :param how: Направление сортировки
        :type how: str

        :param sort: Тип сортировки товарных предложений
        :type sort: str

        :param geo_id: Идентификатор региона
        :type geo_id: int or str

        :param remote_ip: Идентификатор региона пользователя
        :type remote_ip: str

        :raises NoGeoIdOrIP: не передан обязательный параметр geo_id или remote_ip
        :raises RedirectTypesParamError: недопустимое значение параметра redirect_types
        :raises SearchTypeParamError: недопустимое значение параметра search_type
        :raises FieldsParamError: недопустимое значение параметра fields
        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page
        :raises HowParamError: недопустимое значение параметра how
        :raises SortParamError: недопустимое значение параметра sort

        :return: Список параметров редиректа (перенаправления), подходящих под заданные в запросе условия.
        :rtype: response.Redirect

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/redirect-controller-v2-redirect-docpage/
        """
        params = {'text': text}

        if geo_id is None and remote_ip is None:
            raise NoGeoIdOrIP(
                "You must provide either geo_id or remote_ip")

        if geo_id:
            params['geo_id'] = geo_id

        if remote_ip:
            params['remote_ip'] = remote_ip

        if redirect_types:
            for field in redirect_types.split(','):
                if field not in (
                        'CATALOG', 'MODEL', 'SEARCH',
                        'VENDOR', 'ALL'):
                    raise RedirectTypesParamError('"redirect_types" param is wrong')
            params['redirect_types'] = redirect_types

        # todo Ограничение. Параметр действует только, если не указан search_type
        if barcode:
            params['barcode'] = barcode

        if search_type:
            if search_type not in (
                    'BARCODE', 'ISBN', 'TEXT'):
                raise SearchTypeParamError('"search_type" param is wrong')
            params['search_type'] = search_type

        if category_id:
            params['category_id'] = category_id

        if hid:
            params['hid'] = hid

        if fields:
            params['fields'] = self._validate_fields(fields,
                                                     ('CATEGORY_PARENT', 'CATEGORY_STATISTICS', 'CATEGORY_WARNINGS',

                                                      'FILTERS', 'FOUND_CATEGORIES',

                                                      'MODEL_CATEGORY', 'MODEL_DEFAULT_OFFER', 'MODEL_DISCOUNTS',
                                                      'MODEL_FACTS', 'MODEL_FILTER_COLOR', 'MODEL_MEDIA',
                                                      'MODEL_NAVIGATION_NODE',
                                                      'MODEL_OFFERS', 'MODEL_PHOTO', 'MODEL_PHOTOS',
                                                      'MODEL_PRICE', 'MODEL_RATING', 'MODEL_SPECIFICATION',
                                                      'MODEL_VENDOR', 'OFFER_ACTIVE_FILTERS', 'OFFER_CATEGORY',
                                                      'OFFER_DELIVERY', 'OFFER_DISCOUNT',
                                                      'OFFER_OFFERS_LINK', 'OFFER_OUTLET', 'OFFER_OUTLET_COUNT',
                                                      'OFFER_PHOTO', 'OFFER_SHOP',
                                                      'OFFER_VENDOR', 'SHOP_ORGANIZATION', 'SHOP_RATING', 'SORTS',
                                                      'VENDOR_CATEGORIES',
                                                      'VENDOR_TOP_CATEGORIES', 'ALL', 'CATEGORY_ALL', 'MODEL_ALL',
                                                      'OFFER_ALL', 'SHOP_ALL',
                                                      'STANDARD', 'VENDOR_ALL'))

        if user_agent:
            params['user_agent'] = user_agent

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        if how:
            if how not in ('ASC', 'DESC'):
                raise HowParamError('"how" param is wrong')
            params['how'] = how

        if sort:
            if sort not in constants.MODEL_SORT:
                raise SortParamError('"sort" param is wrong')
            params['sort'] = sort

        return Redirect(self._request('redirect', None, params))

    def suggestions(self, text, count=10, page=1, pos=None, suggest_types='DEFAULT'):
        """
        Поисковые подсказки

        :param text: Текст запроса
        :type text: str

        :param count: Размер страницы (количество элементов на странице)
        :type count: int

        :param page: Номер страницы
        :type page: int

        :param pos: Позиция курсора в поисковой подсказке
        :type pos: int

        :param suggest_types: Типы поисковых подсказок
        :type suggest_types: str or list[str]

        :raises CountParamError: недопустимое значение параметра count
        :raises PageParamError: недопустимое значение параметра page
        :raises PosParamError: недопустимое значение параметра pos
        :raises SuggestTypesParamError: недопустимое значение параметра suggest_types

        :return: Список поисковых подсказок, подходящих под заданные условия поиска
        :rtype: objects.Suggestions

        .. seealso:: https://tech.yandex.ru/market/monetization/doc/dg-v2/reference/suggest-controller-v2-get-suggest-docpage/
        """
        params = {'text': text}

        if count < 1 or count > 30:
            raise CountParamError('"count" param must be between 1 and 30')
        else:
            params['count'] = count

        if page < 1:
            raise PageParamError('"page" param must be larger than 1')
        else:
            params['page'] = page

        if pos:
            if pos < 0 or pos > 1024:
                raise PosParamError('"pos" param must be between 1 and 30')
            else:
                params['pos'] = pos

        if suggest_types:
            for field in suggest_types.split(','):
                if field not in (
                        'CATALOG', 'MODEL', 'SEARCH',
                        'VENDOR', 'ALL', 'DEFAULT'):
                    raise SuggestTypesParamError('"suggest_types" param is wrong')
            params['suggest_types'] = suggest_types

        return Suggestions(self._request('redirect', None, params))
