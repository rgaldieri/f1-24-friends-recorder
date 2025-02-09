import pymysql
import time

# Database connection settings
db_host = ''
db_user = ''
db_password = ''
db_name = ''

def check_add_to_news(circuit_id, player_name, new_best_lap):
    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    try:
        with connection.cursor() as cursor:
            # Check if player exists
            cursor.execute("SELECT * FROM times INNER JOIN players ON players.player_id = times.player_id_fk WHERE times.circuit_id_fk = %s AND times.player_id_fk != 99 ORDER by times.best_time LIMIT 1", (circuit_id,))
            result = cursor.fetchone()
            if result:
                cursor.execute("SELECT player_id FROM players WHERE display_name = %s", (player_name,))
                result_pID = cursor.fetchone()
                if result_pID:
                    if(new_best_lap < result[2]):
                        if(result[7] == player_name):
                            # Player improved best
                            cursor.execute("""INSERT INTO news (player_id,circuit_id, timest, lap_time, is_best_update) VALUES (%s, %s, %s, %s, %s)
                            """, (result_pID[0], circuit_id, time.time(), new_best_lap, 1))
                            connection.commit()
                        else:
                            # Player stole lap
                            cursor.execute("""INSERT INTO news (player_id,circuit_id, timest, lap_time, is_best_update) VALUES (%s, %s, %s, %s, %s)
                            """, (result_pID[0], circuit_id, time.time(), new_best_lap, 0))
                            connection.commit()
    finally:
        connection.close()

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
            
            check_add_to_news(circuit_id, player_name, best_time)
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
    print("Checking previous best times")
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
                    check_add_to_news(circuit_id, player_name, time_result[0])
                    # Update the database if the local best time is faster
                    cursor.execute("""
                        UPDATE times SET best_time = %s, sector_one = %s, sector_two = %s, sector_three = %s
                        WHERE player_id_fk = %s AND circuit_id_fk = %s
                        """, (local_best_time, local_sector_one, local_sector_two, local_sector_three, player_id, circuit_id))
                print("Success")
            else:
                # Insert new best time if it doesn't exist
                check_add_to_news(circuit_id, player_name, local_best_time)
                cursor.execute("""
                    INSERT INTO times (player_id_fk, circuit_id_fk, best_time, sector_one, sector_two, sector_three)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """, (player_id, circuit_id, local_best_time, local_sector_one, local_sector_two, local_sector_three))
                print("Success")
            connection.commit()
            print("Done")
    finally:
        connection.close()