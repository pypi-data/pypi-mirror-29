PY NS API
=========

|N\|Solid|

What is this repository for?
----------------------------

-  This python3 module is for easy usage of the the NS Train API

How do I get set up?
--------------------

-  Go To `NS API SIte <https://www.ns.nl/ews-aanvraagformulier/?0>`__
-  Subscribe for the NS API (It's free for 50.000 calls a day)
-  Install this script with:

   -  pip3 py\_nsapi --upgrade (or pip py\_nsapi --upgrade )
   -  or
   -  sudo -H pip3 py\_nsapi --upgrade

-  ready to use it!

Repository & Pypi
-----------------

You can find the Repro at
`Bitbucket <https://bitbucket.org/tvdsluijs/py-nsapi/>`__

and the install information on
`Pypi <https://pypi.python.org/pypi/py-nsapi>`__

API's
-----

The API's return the data in a Dictionary. You can loop through the Dict
as any Dict.

See examples about how to get information.

All api's can write warnings, errors and debug information to log files

Just use

.. code:: python3

    import logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

More information about
`logging <https://docs.python.org/3/howto/logging.html>`__

Storingen
~~~~~~~~~

De webservice voor de storingen en werkzaamheden maakt het mogelijk
informatie op te vragen over storingen en/of werkzaamheden.

Fields
^^^^^^

-  id
-  Traject
-  Reden
-  Periode
-  Bericht
-  Advies

Example code
^^^^^^^^^^^^

.. code:: python3

    from py_nsapi import storingen
    user = "yourusername"
    pwd  = "yournotsoeasytoguesspassword"
    station = [a station, can be empty]
    actual = [true or false]
    unplanned = [true or false] #false = the oposite of what you think! :-) you get unplanned
    ns = reisadviezen(user,pwd)
    ns = storingen(user,pwd)
    nsStoringen = ns.getData(station,  actual, unplanned)

nsStoringen is a Dict

Reisadviezen
~~~~~~~~~~~~

De webservice voor de reisadviezen maakt het mogelijk de NS Reisplanner
aan te roepen voor een treinreis van een station naar een station. Een
reisadvies bestaat uit meerdere reismogelijkheden, zodat de
treinreiziger hier een keuze uit kan maken. Een reismogelijkheid bevat
zowel geplande als actuele informatie.

Fields
^^^^^^

-  AantalOverstappen
-  ActueleVertrekTijd
-  GeplandeAankomstTijd
-  ActueleReisTijd
-  GeplandeVertrekTijd
-  GeplandeReisTijd
-  Status
-  ActueleAankomstTijd
-  Optimaal
-  ReisDeel

   -  @reisSoort
   -  Status
   -  Vervoerder
   -  VervoerType
   -  RitNummer
   -  ReisStop

      -  Naam
      -  Tijd
      -  Spoor

         -  #text
         -  @wijziging

Example code
^^^^^^^^^^^^

.. code:: python3

    from py_nsapi import reisadviezen
    user = "yourusername"
    pwd  = "yournotsoeasytoguesspassword"
    ns = reisadviezen(user,pwd)
    fromST  = "GS"
    toST    = "RTB"
    triplist = ns.getData(fromST, toST)

Stationslijst
~~~~~~~~~~~~~

De webservice voor de stationslijst maakt het mogelijk om alle
stationsnamen op te vragen.

Fields
^^^^^^

-  Code
-  UICCode
-  Synoniemen
-  Type
-  Land
-  Lon
-  Lat
-  Namen

   -  Lang
   -  Middel
   -  Kort

Example code
^^^^^^^^^^^^

.. code:: python3

    from py_nsapi import stations


    user = "yourusername"
    pwd  = "yournotsoeasytoguesspassword"

    ns = stations(user, pwd)
    nsStations = ns.getData()

Vertrektijden
~~~~~~~~~~~~~

De webservice voor de actuele vertrektijden maakt het mogelijk om voor
een station een actueel overzicht op te vragen van alle vertrekkende
treinen voor het komende uur.

Fields
^^^^^^

-  RitNummer
-  EindBestemming
-  Vervoerder
-  VertrekSpoor

   -  #text
   -  @wijziging

-  RouteTekst
-  VertrekTijd
-  TreinSoort

Example code
^^^^^^^^^^^^

.. code:: python3

    from py_nsapi import vertrektijden
    user = "yourusername"
    pwd  = "yournotsoeasytoguesspassword"
    ns = vertrektijden(user,pwd)

    fromST = "GS"
    triplist = ns.getData(fromST)

Prijzen API
~~~~~~~~~~~

De webservice voor de prijzen maakt het mogelijk voor een treinreis de
bijbehorende prijsinformatie op te vragen.

Voor gebruik van de webservice is aparte autorisatie vereist. Deze
autorisatie wordt verleend na ontvangst van een getekend contract. Dit
contract is op te vragen via nsr.api@ns.nl.

Fields
^^^^^^

-  @naam
-  Tariefeenheden
-  ReisType
-  @naam
-  ReisKlasse

   -  @klasse
   -  Korting

      -  Kortingsprijs

         -  @name
         -  @prijs

      -  Totaal
      -  Prijsdeel

         -  @naar
         -  @vervoerder
         -  van
         -  @prijs

Example code
^^^^^^^^^^^^

.. code:: python3

    from py_nsapi import prijzen
    user = "yourusername"
    pwd  = "yournotsoeasytoguesspassword"
    ns = prijzen(user,pwd)

    fromST = "GS"
    toST = "RTB"
    viaST = ""
    dateTime= ""
    data = ns.getData(fromST, toST, viaST, dateTime)

    elements = data['VervoerderKeuzes']
    print(elements) #dict

Who do I talk to?
-----------------

-  Theodorus van der Sluijs (friends call me Theo)
-  theodorus@vandersluijs.nl

License
-------

Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

You are free to:
~~~~~~~~~~~~~~~~

-  Share — copy and redistribute the material in any medium or format
-  Adapt — remix, transform, and build upon the material

-The licensor cannot revoke these freedoms as long as you follow the
license terms.-

Under the following terms:
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Attribution — You must give appropriate credit, provide a link to the
   license, and indicate if changes were made. You may do so in any
   reasonable manner, but not in any way that suggests the licensor
   endorses you or your use.
-  NonCommercial — You may not use the material for commercial purposes.
-  ShareAlike — If you remix, transform, or build upon the material, you
   must distribute your contributions under the same license as the
   original.

NS Disclaimer
-------------

De getoonde prijsinformatie is niet afkomstig van NS reizigers B.V. of
een hieraan gelieerde partij. Jegens NS Reizigers B.V. of daaraan
gelieerde partijen, kunnne dan ook geen rechten worden ontleend met
betrekking tot deze prijsinformatie

Special thanks to
-----------------

Stefan de Konink who gave me a complete new insight with his `python
api <https://github.com/NS-API/Python-API>`__

.. |N\|Solid| image:: https://www.ns.nl/static/generic/2.19.0/images/nslogo.svg
   :target: https://www.ns.nl/reisinformatie/ns-api
