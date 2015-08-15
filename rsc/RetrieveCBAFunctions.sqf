_arr = [];
"
    '
      _arr pushBack (''CBA_fnc_'' + (configName _x));
      false
    ' configClasses _x;
    false
" configClasses (configFile >> "CfgFunctions" >> "CBA");
_arr sort true;
copyToClipboard str(_arr);
