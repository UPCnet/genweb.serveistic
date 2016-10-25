from mock import Mock
import datetime

indicadors = [
    Mock(
        identifier="id-1",
        date_modified="1/2/2015",
        description="Indicador 1",
        categories=[
            Mock(
                description="Categoria 1.1",
                value="v1.1",
                is_online=True,
                frequency=None,
                date_modified="2/2/2015"),
            Mock(
                description="Categoria 1.2",
                value="v1.2",
                is_online=False,
                frequency='Dia',
                date_modified="3/2/2015"),
            ]
        ),
    Mock(
        identifier="id-2",
        date_modified="4/2/2015",
        description="Indicador 2",
        categories=[
            Mock(
                description="Categoria 2.1",
                value="v2.1",
                is_online=False,
                frequency='Mes',
                date_modified="5/2/2015"),
            Mock(
                description="Categoria 2.2",
                value="v2.2",
                is_online=True,
                frequency=None,
                date_modified="6/2/2015"),
            Mock(
                description="Categoria 2.3",
                value="v2.3",
                is_online=True,
                frequency=None,
                date_modified="7/2/2015"),
            ]
        ),
    ]

indicators_dto = [
    Mock(
        identifier='id-1',
        description='Indicador 1',
        date_modified=datetime.datetime(2015, 2, 1, 15, 30, 0),
    )
]

categories_dto = [
    Mock(
        identifier='id-1',
        description='Categoria 1.1',
        type='deferit',
        frequency=None,
        value='v1.1',
        date_modified=datetime.datetime(2015, 2, 2, 15, 30, 0),
    )
]
