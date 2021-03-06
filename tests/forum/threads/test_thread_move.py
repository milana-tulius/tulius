from tulius.forum.threads import models


def test_thread_move(superuser, user):
    # create root source room
    response = superuser.put(
        '/api/forum/', {
            'title': 'source', 'body': 'source description',
            'room': True, 'default_rights': models.ACCESS_READ,
            'granted_rights': []})
    assert response.status_code == 200
    source_room = response.json()
    # create root target room
    response = superuser.put(
        '/api/forum/', {
            'title': 'target', 'body': 'target description',
            'room': True, 'default_rights': models.ACCESS_READ,
            'granted_rights': []})
    assert response.status_code == 200
    target = response.json()
    # create room for move
    response = superuser.put(
        source_room['url'], {
            'title': 'room', 'body': 'room description',
            'room': True, 'default_rights': None, 'granted_rights': []})
    assert response.status_code == 200
    room = response.json()
    # check can't move inside yourself
    response = superuser.put(
        source_room['url'] + 'move/', {
            'parent_id': room['id']})
    assert response.status_code == 403
    # check not privileged user can't move
    response = user.put(
        room['url'] + 'move/', {'parent_id': target['id']})
    assert response.status_code == 403
    # add target write rights
    response = superuser.post(
        target['url'] + 'granted_rights/', {
            'user': {'id': user.user.pk},
            'access_level': models.ACCESS_WRITE
        }
    )
    assert response.status_code == 200
    # check that it is still not enough
    response = user.put(
        room['url'] + 'move/', {'parent_id': target['id']})
    assert response.status_code == 403
    # add room moderate rights
    response = superuser.post(
        room['url'] + 'granted_rights/', {
            'user': {'id': user.user.pk},
            'access_level': models.ACCESS_MODERATE
        }
    )
    assert response.status_code == 200
    # check now it works
    response = user.put(
        room['url'] + 'move/', {'parent_id': target['id']})
    assert response.status_code == 200
    # check how it all looks like now
    response = user.get(target['url'])
    assert response.status_code == 200
    data = response.json()
    assert len(data['rooms']) == 1
    assert data['rooms'][0]['id'] == room['id']
    response = user.get(source_room['url'])
    assert response.status_code == 200
    data = response.json()
    assert len(data['rooms']) == 0
