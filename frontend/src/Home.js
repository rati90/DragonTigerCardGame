import React, { useEffect, useState } from "react";
import axios from "axios";

const Home = () => {
  const [games, setGames] = useState([]);

  // getGames agzavnis requests chvenst apistan romlis misamartia api/get/all/game da mogvaqvs magidis shesaxeb informacia rasac vinaxavt setGames it
  const getGames = async () => {
    const response = await axios.get("http://localhost:8000/allgames");
    setGames(response.data);
  };

  // es renderi moxdeba tuara srazu simon agzavnis requests anu zemota logikas simon
  useEffect(() => {
    getGames();
  }, []);

  const renderGames = () => {
    // roca game is data davimaxsovret eg iyo listi es warmoidginet rogorc for cikli da amogvaq tito mokled rac shedegad gvadzlevs magidis saxels da id
    return games.map((game) => {
      return (
        <div>
          <h1>Game Name: {game.name}</h1>
          <h2>Game ID: {game._id}</h2>
          <a href={`http://localhost:3000/game/${game._id}`}> Go in </a>
          <p> ------------------------------- </p>
        </div>
      );
    });
  };


  return (
    <div>
      <h1>
        Home
        {renderGames()}
      </h1>
    </div>
  );
};

// vso magia dalshe uberet kitxvebis shemtxvevashi momweret imedia gipasuxebt mara didi imedi mainc nu geqnebat mainc ravici :DDDDDDDDDD he shecxet axla
//  tu eseti ragac amoagdo Attempted import error: 'useParams' is not exported from 'react-router'. mashin daweret npm i react-router-dom
export default Home;
