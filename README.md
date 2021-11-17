<p align="center">
    <img src="./img/logo.png">
</p>

<h2 align="center">Google Maps Crawler using Selenium</h2>

<p align="center">
<a href="https://guicommits.com/antifragile-dev-1-restaurant-directory-listing-proposal/"><img alt="antifragile project" src="https://img.shields.io/badge/%F0%9F%A7%91%E2%80%8D%F0%9F%92%BB-antifragile--dev-green"></a>
<img alt="python version" src="https://img.shields.io/badge/python-3.9%20%7C%203.10-blue">
<a href="https://github.com/guilatrova/gmaps-crawler/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/guilatrova/gmaps-crawler"/></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"/></a>
<a href="https://github.com/guilatrova/tryceratops"><img alt="try/except style: tryceratops" src="https://img.shields.io/badge/try%2Fexcept%20style-tryceratops%20%F0%9F%A6%96%E2%9C%A8-black" /></a>
<a href="https://open.vscode.dev/guilatrova/gmaps-crawler"><img alt="Open in Visual Studio Code" src="https://open.vscode.dev/badges/open-in-vscode.svg"/></a>
<a href="https://twitter.com/intent/user?screen_name=guilatrova"><img alt="Follow guilatrova" src="https://img.shields.io/twitter/follow/guilatrova?style=social"/></a>
</p>

> Built as part of the [Antifragile Dev Project](https://guicommits.com/antifragile-dev-1-restaurant-directory-listing-proposal/)

Selenium crawler that browses Google Maps as a regular user and stores the data in an object.

---

## Sample

![Sample](img/gmaps-crawler-sample.gif)

## Extracted data example:

```py
 Place(                                                                                                            │ │
│ │ │   name='Pizza Me Santos',                                                                                    │ │
│ │ │   address='Av. Washington Luis, 565 - loja 05 - Boqueirão, Santos - SP, 11055-001',                          │ │
│ │ │   business_hours={                                                                                           │ │
│ │ │   │   'Wednesday': '6–10:30PM',                                                                              │ │
│ │ │   │   'Thursday': '6–10:30PM',                                                                               │ │
│ │ │   │   'Friday': '6–11PM',                                                                                    │ │
│ │ │   │   'Saturday': '6–11PM',                                                                                  │ │
│ │ │   │   'Sunday': '6–10:30PM',                                                                                 │ │
│ │ │   │   'Monday': '6–10:30PM',                                                                                 │ │
│ │ │   │   'Tuesday': '6–10:30PM'                                                                                 │ │
│ │ │   },                                                                                                         │ │
│ │ │   photo_link='https://lh5.googleusercontent.com/p/AF1QipMyVkKioODaU0A_ogHPXosm_QcMndZN6I6YHIDo=w408-h272-k-no│ │
│ │ │   rate='5.0',                                                                                                │ │
│ │ │   reviews='16 reviews',                                                                                      │ │
│ │ │   extra_attrs={                                                                                              │ │
│ │ │   │   'Menu': 'Menu\npizzame-santos.goomer.app',                                                             │ │
│ │ │   │   'Website: pizzame-santos.goomer.app ': 'pizzame-santos.goomer.app',                                    │ │
│ │ │   │   'Phone: (13) 3385-0059 ': '(13) 3385-0059',                                                            │ │
│ │ │   │   'Plus code: 2MHC+WF Boqueirão, Santos - State of São Paulo': '2MHC+WF Boqueirão, Santos - State of São │ │
│ │ Paulo'                                                                                                         │ │
│ │ │   },                                                                                                         │ │
│ │ │   traits={                                                                                                   │ │
│ │ │   │   'Service options': ['No-contact delivery', 'Delivery', 'Takeaway', 'Dine-in'],                         │ │
│ │ │   │   'Accessibility': ['Wheelchair-accessible entrance'],                                                   │ │
│ │ │   │   'Offerings': ['Organic dishes', 'Vegetarian options'],                                                 │ │
│ │ │   │   'Dining options': ['Dessert'],                                                                         │ │
│ │ │   │   'Amenities': ['Good for kids'],                                                                        │ │
│ │ │   │   'Atmosphere': ['Casual'],                                                                              │ │
│ │ │   │   'Crowd': ['Groups'],                                                                                   │ │
│ │ │   │   'Planning': ['Accepts reservations'],                                                                  │ │
│ │ │   │   'Payments': ['Credit cards']                                                                           │ │
│ │ │   }                                                                                                          │ │
│ │ )
```
