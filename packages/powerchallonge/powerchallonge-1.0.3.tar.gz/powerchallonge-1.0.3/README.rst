powerchallonge
**************
.. image:: https://travis-ci.org/m3fh4q/powerchallonge.svg?branch=master
    :target: https://travis-ci.org/m3fh4q/powerchallonge

powerchallonge is a client libary for the `Challonge.com API <https://api.challonge.com/v1>`_.

All the API Methods are supported.

.. contents:: 

Python version compatibility
############################

- 2.7
- 3.3+

Dependencies
############
-  **requests**

Installation
############
::
    
    pip install powerchallonge

Basic usage
###########
.. code:: python

    import challonge

    #Configure your settings
    api_key = 'YOURCHALLONGEAPIKEY'
    challonge.set_user_settings(api_key)
    

    #Retrieve a set of tournaments created with your account as a Python list of dictionaries
    tournaments = challonge.tournaments.index()
    for tournament in tournaments:
        print(tournament['name'], tournament['id'])

    #Retrieve a single tournamentas a Python dictionnary using it's id or challonge like url
    tournament = challonge.tournaments.show(1234)
    print(tournament['name'], tournament['game_name'])

Known Issues
############
- After a participant is checked in using participants.check_in(), the 'checked_in' field remains False but the participant is properly checked in on the site
- This problem doesn't appear for the participants.undo_check_in(), the field is properly set from True to False when using it
- Challonge API returns error 500 when Creatin/Updating a match_attachment asset
- When using match_attachments.update(), the updated field does not seem to get changed when doing a verification with match_attachments.show(), however the update is effective and shows up correctly on the site

All these issues have been reported to challonge.

Running the tests
#################
The tests/tests.py script verifies functionality for all the API Methods (except the ones with known issues) and powerchallonge specific functions such as settings configuring and both json and xml conversion functions.

**How to run the tests:**

- Set a CHALLONGE_API_KEY environment variable
- From the repository's root directory

::

    python -m unittest discover -s tests -p "tests.py" -v



Advanced usage
##############

Passing parameters
==================
Some methods only have positional arguments, some require the keyword argument 'params'

params should be a dictionnary of the parameters you intend to use in the method.

.. code:: python

    myparams = {'subdomain': my_subdomain}
    subdomain_tournaments = challonge.tournaments.index(params=myparams)

    myparams2 = {'name': 'tournament1', 'url': 'tournament123123129032901'}
    tournament1 = challonge.tournaments.create(params=myparams2)



Advanced user settings
======================
By default, you only need your api key and the set_user_settings() function to use powerchallonge.

You can use set_user_settings_advanced() for more customization

The variables below are the default settings if set_user_settings_advanced() isn't called.

.. code:: python

    api_key = "YOURCHALLONGEAPIKEY"  # Your Challonge API key

    easy_tournament_identifier = False
    # True to use full URLs for referring to tournaments
    # instead of challonge like URLs.
    # false to use regular challonge API like URLs.

    query_type = ".json"
    # The desired response expected from the challonge API, '.json' or '.xml'

    raw_response = False
    # The desired response, False for python like objects : lists, dictionnaries.
    # True for raw response from the API in the form of a Requests Response Object
    # http://docs.python-requests.org/en/master/api/#requests.Response

    #Apply the settings
    challonge.set_user_settings_advanced(api_key, easy_tournament_identifier,
                                         query_type,
                                         raw_response, verbose_level, test_mode)


Convert xml and json files to params
====================================

powerchallonge comes with tools to convert json or xml files to a dictionnary that can be used agument in the API methods.
This allows the user to create custom templates for specific tournaments and save them as .json or .xml and load them easily.

the functions only supports single parent type json/xml files the childs will be the key:elements in the dictionnary

.. code:: python

    myparams = challonge.json_to_params(path_to_json_file)
    myparams = challonge.xml_to_params(path_to_xml_file)

Elements are always processed as strings or booleans, if you want an element to be a list (only interesting in the case of participants.bulk_add() ) use the following in your xml file :

::

    <name type='list'>player1,player2,player3</name>


API Methods examples list
=========================
If raw_response is set to False (default), the output for any API method used will be a Python object.

If raw response is set to True, the output for any API method used will be a requests response object.


Tournaments
-----------
`Tournaments : Index <https://api.challonge.com/v1/documents/tournaments/index>`_.

.. code:: python

    # params argument is optional
    r = challonge.tournaments.index()
    print(r)  # a list of dictionaries of attributes (one dictionary per tournament)


`Tournaments : Create <https://api.challonge.com/v1/documents/tournaments/create>`_.

.. code:: python

    # params argument is optional but necessary (challonge error later on if missing)
    myparams = {'name': 'mytournament123123', 'url': 'mytournament123123'}
    myparams['start_at']="2020/02/16T17:00:00+00:00"
    #If you don't set an offset ("+00:00" above), the hour will be inconsistent
    #Always set your start_time to UTC+your_zone_offset
    r = challonge.tournaments.create(params=myparams)
    print(r)  # a dictionary of the attributes of the tournament

`Tournaments : Show <https://api.challonge.com/v1/documents/tournaments/show>`_.

.. code:: python

    # params argument is optional
    r = challonge.tournaments.show(identifier)
    print(r)  # a dictionary of the attributes of the tournament

`Tournaments : Update <https://api.challonge.com/v1/documents/tournaments/update>`_.

.. code:: python
    
    # params argument is optional but necessary (challonge error later on if missing)
    myparams{'description': 'new_description'}
    r = challonge.tournaments.update(identifier, params=myparams)
    print(r)  # a dictionary of the attributes of tournament

`Tournaments : Destroy <https://api.challonge.com/v1/documents/tournaments/destroy>`_.

.. code:: python

    # no params argument required
    r = challonge.tournaments.destroy(identifier)
    print(r)  # a dictionary of the attributes of the tournament

`Tournaments : Process Check-ins <https://api.challonge.com/v1/documents/tournaments/process_check_ins>`_.

.. code:: python

    # params argument is optional
    r = challonge.tournaments.process_check_ins(identifier)
    print(r)  # a dictionary of the attributes of the tournament

`Tournaments : Abort Check-in <https://api.challonge.com/v1/documents/tournaments/abort_check_in>`_.

.. code:: python

    # params argument is optional
    r = challonge.tournaments.abort_check_ins(identifier)
    print(r)  # a dictionary of the attributes of the tournament

`Tournaments : Start <https://api.challonge.com/v1/documents/tournaments/start>`_.

.. code:: python

    # params argument is optional
    r = challonge.tournaments.start(identifier)
    print(r)  # a dictionary of the attributes of the tournament

`Tournaments : Finalize <https://api.challonge.com/v1/documents/tournaments/finalize>`_.

.. code:: python

    # params argument is optional
    r = challonge.tournaments.finalize(identifier)
    print(r)  # a dictionary of the attributes of the tournament

`Tournaments : Reset <https://api.challonge.com/v1/documents/tournaments/reset>`_.


Participants
------------
.. code:: python

    # params argument is optional
    r = challonge.tournaments.reset(identifier)
    print(r)  # a dictionary of the attributes of the tournament

`Participants : index <https://api.challonge.com/v1/documents/participants/index>`_.

.. code:: python

    # params argument is optional
    r = challonge.participants.index(identifier)
    print(r)  # a list of dictionnaries of attributes (one dictionnary per participant)

`Participants : Create <https://api.challonge.com/v1/documents/participants/create>`_.

.. code:: python

    # params argument is optional but necessary (challonge error later on if missing)
    myparams = {'name': 'player1'}
    r = challonge.participants.create(identifier, params=myparams)
    print(r)  # a dictionary of the attributes of the participant

`Participants : Bulk-Add <https://api.challonge.com/v1/documents/participants/bulk_add>`_.

.. code:: python

    # params argument is optional but necessary (challonge error later on if missing)
    # For the bulk_add to work, the 'name' field of params must be a list of the names
    myparams = {'name': ['player1', 'player2', 'player3']}
    r = challonge.participants.bulk_add(identifier, params=myparams)
    print(r)  # a list of dictionnaries of attributes (one dictionnary per added participant)

`Participants : Show <https://api.challonge.com/v1/documents/participants/show>`_.

.. code:: python

    # params argument is optional
    r = challonge.participants.show(identifier, participant_id)
    print(r)  # a dictionary of the attributes of the participant


`Participants : Update <https://api.challonge.com/v1/documents/participants/update>`_.

.. code:: python

    # params argument is optional but necessary (challonge error later on if missing)
    myparams = {'name': 'player1_update'}
    r = challonge.participants.update(identifier, participant_id, params=myparams)
    print(r)  # a dictionary of the attributes of the participant

`Participants : Check-in <https://api.challonge.com/v1/documents/participants/check_in>`_.

.. code:: python

    # no params argument required
    r = challonge.participants.check_in(identifier, participant_id)
    print(r)  # a dictionary of the attributes of the participant
    #The participant is properly checked-in on the site
    #But the 'checked_in' field will still be set to False, check Known Issues


`Participants : Undo Check In <https://api.challonge.com/v1/documents/participants/undo_check_in>`_.

.. code:: python

    # no params argument required
    r = challonge.participants.undo_check_in(identifier, participant_id)
    print(r)  # a dictionary of the attributes of the participant

`Participants : Destroy <https://api.challonge.com/v1/documents/participants/destroy>`_.

.. code:: python

    # no params argument required
    r = challonge.participants.destroy(identifier, participant_id)
    print(r)  # a dictionary of the attributes of the participant

`Participants : Randomize <https://api.challonge.com/v1/documents/participants/randomize>`_.

.. code:: python

    # no params argument required
    r = challonge.participants.randomize(identifier)
    print(r)  # a list of dictionnaries of attributes (one dictionary per participant)


Matches
-------
`Matches : Index <https://api.challonge.com/v1/documents/matches/index>`_.

.. code:: python

    # params argument is optional
    r = challonge.matches.index(identifier)
    print(r)  # a list of dictionaries of attributes (one dictionary per match)

`Matches : Show <https://api.challonge.com/v1/documents/matches/show>`_.

.. code:: python

    # params argument is optional
    r = challonge.matches.show(identifier, match_id)
    print(r)  # a dictionary of the attributes of the match

`Matches : Update <https://api.challonge.com/v1/documents/matches/update>`_.

.. code:: python

    # params argument is optional but necessary (challonge error later on if missing)
    myparams = {'scores_csv': '1-0'}
    r = challonge.matches.update(identifier, match_id, params=myparams)
    print(r)  # a dictionary of the attributes of the match

`Matches : Reopen <https://api.challonge.com/v1/documents/matches/reopen>`_.

.. code:: python

    # no params argument required
    r = challonge.matches.reopen(identifier, match_id)
    print(r)  # a dictionary of the attributes of the match

`Match Attachments : Index <https://api.challonge.com/v1/documents/match_attachments/index>`_.

.. code:: python

    # no params argument required
    r = challonge.match_attachments.index(identifier, match_id)
    print(r)  # a list of dictionaries of attributes (one dictionary per match attachment)


Match Attachments
-----------------
`Match Attachments : Create <https://api.challonge.com/v1/documents/match_attachments/create>`_.

.. code:: python

    #Doesn't work if asset is a file (Error 500, check known issues)
    # params argument is optional but necessary (challonge error later on if missing)
    myparams = {'description': 'description'}
    r = challonge.match_attachments.create(identifier, match_id, params=myparams)
    print(r)  # a dictionary of the attributes of the match attachment

`Match Attachments : Show <https://api.challonge.com/v1/documents/match_attachments/show>`_.

.. code:: python

    # no params argument required
    r = challonge.match_attachments.show(identifier, match_id, attachment_id)
    print(r)  # a dictionary of the attributes of the match attachment

`Match Attachments : Update <https://api.challonge.com/v1/documents/match_attachments/update>`_.

.. code:: python

    # params argument is optional but necessary (challonge error later on if missing)
    myparams = {'description': 'new_description'}
    r = challonge.match_attachments.update(identifier, match_id, attachment_id, params)
    print(r)  # a dictionary of the attributes of the match attachment
    #the updated field does not seem to get changed when doing a verification 
    #with match_attachments.show(), 
    #however the update is effective and shows up correctly on the site

`Match Attachments : Destroy <https://api.challonge.com/v1/documents/match_attachments/destroy>`_.

.. code:: python

    # no params argument required
    r = challonge.match_attachments.destroy(identifier, match_id, attachment_id)
    print(r)  # a dictionary of the attributes of the match attachment










