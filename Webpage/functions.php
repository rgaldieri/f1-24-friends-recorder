<?php

  function format_time($mills) {
    $milliseconds = abs($mills);

    $minutes = floor($milliseconds / 60000);
    $seconds = floor(($milliseconds % 60000) / 1000);
    $millis = $milliseconds % 1000;

    $formatted_time = $minutes > 0 
        ? sprintf('%d.%02d.%03d', $minutes, $seconds, $millis) 
        : sprintf('%02d.%03d', $seconds, $millis);

    return $mills < 0 ? '-' . $formatted_time : $formatted_time;
  }

function generateMedals($db) {
    // SQL query to retrieve players' names and the number of circuits where they are fastest
    $sql = "SELECT p.display_name, COUNT(DISTINCT t.circuit_id_fk) AS fastest_circuits FROM players p 
            JOIN times t ON p.player_id = t.player_id_fk 
            JOIN ( 
                SELECT circuit_id_fk, MIN(best_time) AS fastest_time 
                FROM times 
                WHERE player_id_fk != 99 
                GROUP BY circuit_id_fk 
            ) fastest 
            ON t.circuit_id_fk = fastest.circuit_id_fk AND t.best_time = fastest.fastest_time 
            WHERE NOT p.player_id = 99 
            GROUP BY p.display_name 
            ORDER BY fastest_circuits DESC";

    $result = $db->getConnection()->query($sql);

    if ($result->num_rows > 0) {
        // Fetch the second best time
        $result->data_seek(1);
        $row_two = $result->fetch_assoc();
        echo '
        <div class="record-holder">
            <img class="medal medal-second" src="images/Second.png"/>
            <p class="record-holder-name">' . htmlspecialchars($row_two['display_name']) . '</p>
            <p class="record-count">' . htmlspecialchars($row_two['fastest_circuits']) . ' records</p>
        </div>';

        // Fetch the best time
        $result->data_seek(0);
        $row = $result->fetch_assoc();
        echo '
        <div class="record-holder">
            <img class="medal medal-first" src="images/First.png"/>
            <p class="record-holder-name pos-scnd">' . htmlspecialchars($row['display_name']) . '</p>
            <p class="record-count">' . htmlspecialchars($row['fastest_circuits']) . ' records</p>
        </div>';

        // Fetch the third best time
        $result->data_seek(2);
        $row_three = $result->fetch_assoc();
        echo '
        <div class="record-holder">
            <img class="medal medal-third" src="images/Third.png"/>
            <p class="record-holder-name">' . htmlspecialchars($row_three['display_name']) . '</p>
            <p class="record-count">' . htmlspecialchars($row_three['fastest_circuits']) . ' records</p>
        </div>';
    } else {
        echo "0 results";
    }
  }

  function PopulateNews($db){
        // SQL query to retrieve players' names and the number of circuits where they are fastest
  	$sql = "SELECT news.timest, news.lap_time, news.is_best_update, circuit.circuit_name, players.display_name FROM news JOIN players ON news.player_id = players.player_id JOIN circuit ON news.circuit_id = circuit.circuit_id ORDER BY news.timest DESC LIMIT 10";
  	$result = $db->getConnection()->query($sql);
  	if ($result->num_rows > 0) {
  		while ($news_row = $result->fetch_assoc()) {
  			if($news_row['is_best_update'] == 1){
  				$r = rand(0,3);
  				switch ($r) {
  					case 0:
  					echo '<p>'.date('d/m/Y - H:i', $news_row['timest']).' - <b>'.$news_row['display_name'].'</b> improved the record on <b>'.$news_row['circuit_name'].'</b></p>';                  
  					break;
  					case 1:
  					echo '<p>'.date('d/m/Y - H:i', $news_row['timest']).' - <b>'.$news_row['display_name'].'</b> raised the bar even higher on <b>'.$news_row['circuit_name'].'</b></p>';                  
  					break;
  					case 2:
  					echo '<p>'.date('d/m/Y - H:i', $news_row['timest']).' - <b>'.$news_row['display_name'].'</b> set a new PB on <b>'.$news_row['circuit_name'].'</b>, as if it wasn\'t enough already....</p>';                  
  					break;
  					case 3:
  					echo '<p>'.date('d/m/Y - H:i', $news_row['timest']).' - <b>'.$news_row['display_name'].'</b> is one step closer to WR in <b>'.$news_row['circuit_name'].'</b></p>';                  
  					break;
  					default:
  					echo '';
  				}
  			} else {
  				$r = rand(0,3);
  				switch ($r) {
  					case 0:
  					echo '<p>'.date('d/m/Y - H:i', $news_row['timest']).' - <b>'.$news_row['display_name'].'</b> stole the record on <b>'.$news_row['circuit_name'].'</b></p>';                  
  					break;
  					case 1:
  					echo '<p>'.date('d/m/Y - H:i', $news_row['timest']).' - <b>'.$news_row['display_name'].'</b> now OWNS <b>'.$news_row['circuit_name'].'</b></p>';                  
  					break;
  					case 2:
  					echo '<p>'.date('d/m/Y - H:i', $news_row['timest']).' - <b>'.$news_row['circuit_name'].'</b> should be renamed after <b>'.$news_row['display_name'].'</b></p>';              
  					break;
  					case 3:
  					echo '<p>'.date('d/m/Y - H:i', $news_row['timest']).' - <b>'.$news_row['display_name'].'</b> and <b>'.$news_row['circuit_name'].'</b> are a match made in heaven</p>';                  
  					break;
  					default:
  					echo'';
  				}
  			}
  		}
  	}
  }

  function getCircuits($db) {
    $sql = "SELECT circuit_id, circuit_name, country_name, image_url, sorting_order 
    FROM circuit ORDER BY sorting_order";
    $result = $db->getConnection()->query($sql);

    if ($result === false) {
      die("Error executing query: " . $db->getConnection()->error);
    }

    return $result;
  }

  function getFastestTimes($db, $circuit_id) {
    $sql = $db->getConnection()->prepare(
      "SELECT p.display_name, t.best_time, t.sector_one, t.sector_two, t.sector_three 
      FROM times t 
      JOIN players p ON t.player_id_fk = p.player_id 
      WHERE t.circuit_id_fk = ? AND NOT p.player_id = 99 
      ORDER BY t.best_time ASC LIMIT 3"
    );
    $sql->bind_param("i", $circuit_id);
    $sql->execute();
    return $sql->get_result();
  }

  function getBestSectors($db, $circuit_id) {
    $result = getFastestTimes($db, $circuit_id);

    $best_s1 = PHP_INT_MAX;
    $best_s2 = PHP_INT_MAX;
    $best_s3 = PHP_INT_MAX;

    while ($row = $result->fetch_assoc()) {
      $best_s1 = min($best_s1, $row['sector_one']);
      $best_s2 = min($best_s2, $row['sector_two']);
      $best_s3 = min($best_s3, $row['sector_three']);
    }

    return ['s1' => $best_s1, 's2' => $best_s2, 's3' => $best_s3];
  }

  function displayTable($circuit, $best_sectors, $times, $is_even) {
    $class = $is_even ? 'left-table-column table-column col-md-6' : 'table-column col-md-6';

    echo '<div class="' . $class . '">
          <div class="circuit-name">
          <span class="circuit-flag-area">
          <img class="flag" src="images/' . $circuit['image_url'] . '.png"/>
          </span>
          <span class="circuit-name-content">
          <p class="country-name">' . $circuit['country_name'] . '</p>
          <p class="venue-name">' . htmlspecialchars($circuit['circuit_name']) . '</p>
          </span>
          </div>';

    echo '<table class="circuit-table">
          <tr class="tr-time">
          <th>Driver</th>
          <th>Time</th>
          <th>S1</th>
          <th>S2</th>
          <th>S3</th>
          <th>Delta</th>
          </tr>';

    $first_best_time = null;
    while ($row = $times->fetch_assoc()) {
        $delta = $first_best_time === null ? "-------" : '+' . format_time($row['best_time'] - $first_best_time);
        $first_best_time = $first_best_time ?? $row['best_time'];

        $s1_class = ($row['sector_one'] == $best_sectors['s1']) ? 'pink' : '';
        $s2_class = ($row['sector_two'] == $best_sectors['s2']) ? 'pink' : '';
        $s3_class = ($row['sector_three'] == $best_sectors['s3']) ? 'pink' : '';

        echo '<tr class="tr-time">
              <td>' . htmlspecialchars($row['display_name']) . '</td>
              <td>' . htmlspecialchars(format_time($row['best_time'])) . '</td>
              <td class="' . $s1_class . '">' . htmlspecialchars(format_time($row['sector_one'])) . '</td>
              <td class="' . $s2_class . '">' . htmlspecialchars(format_time($row['sector_two'])) . '</td>
              <td class="' . $s3_class . '">' . htmlspecialchars(format_time($row['sector_three'])) . '</td>
              <td>' . htmlspecialchars($delta) . '</td>
              </tr>';
    }

    echo '</table></div>';
  }

  function populateTables($db) {
    $circuits = getCircuits($db);

    if ($circuits->num_rows > 0) {
        $even = 1;

        while ($circuit_row = $circuits->fetch_assoc()) {
            $best_sectors = getBestSectors($db, $circuit_row['circuit_id']);
            $times = getFastestTimes($db, $circuit_row['circuit_id']);
            displayTable($circuit_row, $best_sectors, $times, $even % 2 == 0);
            $even++;
        }
    } else {
        echo 'No circuits found.';
    }
  }

?>