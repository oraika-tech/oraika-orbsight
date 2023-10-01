from service.common.infra.redis_provider import EntityRedisProvider

test_entity_manager = EntityRedisProvider(key_prefix='test', host="localhost", port=6379)


def test_single_data_lifecycle():
    # Set Entity
    email_id = 'girish.patel@oraika.com'
    test_entity_manager.set_entity(email_id, {"first_name": "Girish", "last_name": "Patel", "company": "Oraika"}, ttl=180)

    # Get Entity
    stored_data = test_entity_manager.get_entity(email_id)
    print(f"Stored data: {stored_data}")

    assert stored_data is not None
    assert stored_data.get('first_name') == 'Girish'
    assert stored_data.get('last_name') == 'Patel'
    assert stored_data.get('company') == 'Oraika'

    # Update Entity
    test_entity_manager.update_entity(email_id, 'company', 'PlayArena')

    stored_data = test_entity_manager.get_entity(email_id)
    print(f"Stored data: {stored_data}")
    assert stored_data.get('first_name') == 'Girish'
    assert stored_data.get('last_name') == 'Patel'
    assert stored_data.get('company') == 'PlayArena'

    # Delete Entity
    test_entity_manager.delete_entity(email_id)

    stored_data = test_entity_manager.get_entity(email_id)
    print(f"Stored data: {stored_data}")

    assert stored_data == {}
