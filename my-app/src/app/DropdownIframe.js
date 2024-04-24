import React, { useState } from 'react';

function DropdownIframe() {
    const [iframeSrc, setIframeSrc] = useState('http://localhost:8081/db/pokeapi_datawarehouse/');

    const iframes = {
        'Postgres DW': 'http://127.0.0.1:8084/?pgsql=postgres&username=admin&db=pokedw&ns=public/',
        'PokeAPI Datawarehouse': 'http://localhost:8081/db/pokeapi_datawarehouse/',
        'Other Source 2': 'http://localhost:8083/source2/',
    };

    const handleSelectChange = (event) => {
        setIframeSrc(iframes[event.target.value]);
    };

    return (
        <div>
            <p>{iframeSrc}</p>
            <select onChange={handleSelectChange}>
                {Object.keys(iframes).map((key) => (
                    <option key={key} value={key}>
                        {key}
                    </option>
                ))}
            </select>
            <iframe src={iframeSrc} width="1000" height="700" />
        </div>
    );
}

export default DropdownIframe;
