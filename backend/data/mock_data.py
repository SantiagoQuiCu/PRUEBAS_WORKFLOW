marcas = [
    {
        "id": 1,
        "nombre": "Toyota",
        "pais": "Japon",
        "fundacion": 1937
    },
    {
        "id": 2,
        "nombre": "Ford",
        "pais": "Estados Unidos",
        "fundacion": 1903
    },
    {
        "id": 3,
        "nombre": "BMW",
        "pais": "Alemania",
        "fundacion": 1916
    }
]

vehiculos = [
    {
        "id": 1,
        "modelo": "Corolla",
        "anio": 2023,
        "precio": 25000.00,
        "color": "Blanco",
        "marca_id": 1
    },
    {
        "id": 2,
        "modelo": "F-150",
        "anio": 2022,
        "precio": 35000.00,
        "color": "Negro",
        "marca_id": 2
    },
    {
        "id": 3,
        "modelo": "X3",
        "anio": 2024,
        "precio": 45000.00,
        "color": "Azul",
        "marca_id": 3
    },
    {
        "id": 4,
        "modelo": "Camry",
        "anio": 2023,
        "precio": 28000.00,
        "color": "Gris",
        "marca_id": 1
    }
]

reporte_marcas = {
    "total_marcas": 3,
    "total_vehiculos": 4,
    "marcas_por_popularidad": [
        {
            "marca": {
                "id": 1,
                "nombre": "Toyota",
                "pais": "Japon"
            },
            "total_vehiculos": 2,
            "vehiculos": [
                {"modelo": "Corolla", "anio": 2023},
                {"modelo": "Camry", "anio": 2023}
            ]
        },
        {
            "marca": {
                "id": 2,
                "nombre": "Ford",
                "pais": "Estados Unidos"
            },
            "total_vehiculos": 1,
            "vehiculos": [
                {"modelo": "F-150", "anio": 2022}
            ]
        },
        {
            "marca": {
                "id": 3,
                "nombre": "BMW",
                "pais": "Alemania"
            },
            "total_vehiculos": 1,
            "vehiculos": [
                {"modelo": "X3", "anio": 2024}
            ]
        }
    ],
    "marca_mas_activa": {
        "nombre": "Toyota",
        "total_vehiculos": 2
    }
}