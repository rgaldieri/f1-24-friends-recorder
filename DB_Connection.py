import pymysql

# Database connection settings
db_host = ''
db_user = ''
db_password = ''
db_name = ''

def add_best_time(player_name, circuit_id, best_time, sector_one, sector_two, sector_three):
    # Connect to the database
    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    print("Trying to add best time")
    try:
        with connection.cursor() as cursor:
            # Check if player exists
            cursor.execute("SELECT player_id FROM players WHERE display_name = %s", (player_name,))
            result = cursor.fetchone()
            
            if result:
                player_id = result[0]
            else:
                # Insert new player
                cursor.execute("INSERT INTO players (display_name) VALUES (%s)", (player_name,))
                connection.commit()
                player_id = cursor.lastrowid
            
            # Check if an entry exists for the player and circuit combination
            cursor.execute("SELECT * FROM times WHERE player_id_fk = %s AND circuit_id_fk = %s", (player_id, circuit_id))
            result = cursor.fetchone()
            
            if result:
                # Update existing entry
                cursor.execute("""
                    UPDATE times SET best_time = %s, sector_one = %s, sector_two = %s, sector_three = %s
                    WHERE player_id_fk = %s AND circuit_id_fk = %s
                    """, (best_time, sector_one, sector_two, sector_three, player_id, circuit_id))
            else:
                # Insert new entry
                cursor.execute("""
                    INSERT INTO times (player_id_fk, circuit_id_fk, best_time, sector_one, sector_two, sector_three)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """, (player_id, circuit_id, best_time, sector_one, sector_two, sector_three))
            print("Success")
            connection.commit()
    finally:
        connection.close()

def update_best_time_if_faster(player_name, circuit_id, local_best_time, local_sector_one, local_sector_two, local_sector_three):
    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    print("Checking best time")
    try:
        with connection.cursor() as cursor:
            # Check if player exists
            cursor.execute("SELECT player_id FROM players WHERE display_name = %s", (player_name,))
            player_result = cursor.fetchone()

            if player_result:
                player_id = player_result[0]
            else:
                # Insert new player
                cursor.execute("INSERT INTO players (display_name) VALUES (%s)", (player_name,))
                connection.commit()
                player_id = cursor.lastrowid
            
            # Check if best time exists for the player and circuit
            cursor.execute("SELECT best_time FROM times WHERE player_id_fk = %s AND circuit_id_fk = %s", (player_id, circuit_id))
            time_result = cursor.fetchone()
            
            if time_result:
                db_best_time = time_result[0]
                # Compare the local best time with the database best time
                if local_best_time < db_best_time:
                    # Update the database if the local best time is faster
                    cursor.execute("""
                        UPDATE times SET best_time = %s, sector_one = %s, sector_two = %s, sector_three = %s
                        WHERE player_id_fk = %s AND circuit_id_fk = %s
                        """, (local_best_time, local_sector_one, local_sector_two, local_sector_three, player_id, circuit_id))
            else:
                # Insert new best time if it doesn't exist
                cursor.execute("""
                    INSERT INTO times (player_id_fk, circuit_id_fk, best_time, sector_one, sector_two, sector_three)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """, (player_id, circuit_id, local_best_time, local_sector_one, local_sector_two, local_sector_three))
            print("Success")
            connection.commit()
    finally:
        connection.close()