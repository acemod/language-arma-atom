_arr = [];
"
  '
      ''
        _arr pushBack (""BIS_fnc_"" + (configName _x));
        false
      '' configClasses _x;
      false
  ' configClasses _x;
  false
" configClasses (configFile >> "CfgFunctions");
_arr sort true;
copyToClipboard str(_arr);
