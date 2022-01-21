// Import the filesystem module

const fs = require('fs');

// Declare various variables

var fileName = './KOP_Income_Statement.xlsx';
var fileSheetNum = 0;
var headerRowIndx = 3;  // index containing the header row in the excel file
var yearsToRead = [];
yearsToRead[0] = "2021";
yearsToRead[1] = "2022";
yearsToRead[2] = "2023";
var doValuesHaveOppSign = 1;

outPutFileName = 'testData.txt';

// Read KOP Income Statement

var rawTotalResults = [];
var test = $.csv
rawTotalResults = readExcelFile(fileName, fileSheetNum, headerRowIndx);

var rawData = rawTotalResults[1];
var rawHeaderList = rawTotalResults[0];

// Grab only the values that have the specified years in them

var headerListToPrint = [];
var indexListToPrint = [];
var indxCounter = 0;
rawHeaderList.forEach(x => {
    for (var i = 0; i < yearsToRead.length; i++)
    {
        if (x.includes(yearsToRead[i]))
        {
            headerListToPrint.push(x);
            indexListToPrint.push(indxCounter);
        }
    }
    indxCounter = indxCounter + 1;
})

var numMonthsToPrint = headerListToPrint.length;

// Write the header for the output file

headerTxt = "Description,    Date,    Value\n";
fs.writeFile(outPutFileName, headerTxt, { flag: 'w' }, err => {});

for (var i = 0; i < rawData.length; i++)
{
    var row = getRow(rawData, i);

    // Skip this row if there is no data

    var checkValue = row[2];
    if (checkValue == '' && checkValue !== 0)
    {
        continue;
    }

    // Now write out the data for this row

    var discription = row[1];
    for (var k = 0; k < numMonthsToPrint; k++)
    {
        let value = row[indexListToPrint[k]];
        if (doValuesHaveOppSign)
        {
            value = -value;
        }
        fs.appendFileSync(outPutFileName, discription, err => {});
        fs.appendFileSync(outPutFileName, ", \t", err => {});
        fs.appendFileSync(outPutFileName, headerListToPrint[k], err => {});
        fs.appendFileSync(outPutFileName, ", \t", err => {});
        fs.appendFileSync(outPutFileName, value.toString(), err => {});
        fs.appendFileSync(outPutFileName, "\n", err => {});
    }

}


console.log("Done");


// Below is the list of functions used
// -----------------------------------

// Function to read an Excel file and return data in an Array
// The first object contains the header and the second object
// contains the raw data

function readExcelFile(fileName, sheetNum, headerRowIndx)
{
    const reader = require('xlsx');

    const file = reader.readFile(fileName);
    
    const sheets = file.SheetNames
    
    const rawJsonData = reader.utils.sheet_to_json(file.Sheets[file.SheetNames[sheetNum]], {raw: true, defval:""});

    var data = new Array();
    var header = [];

    let j = 0;
    rawJsonData.forEach((res) => {

        j = j + 1;

        if (j == headerRowIndx)
        {

            const rows = Object.keys(res).map(key => [key, res[key]]);

            for (var i = 0; i < rows.length; i++)
             {
                var temp = rows[i];
                 header.push(temp[1]);
            }
        }
        else if (j > headerRowIndx)
        {
            const rows = Object.keys(res).map(key => [key, res[key]]);

            var dd = [];

            let rowLength = rows.length;
            for (var i = 0; i < rowLength; i++)
            {
                var temp = rows[i];
                dd[i] = temp[1];
            }

            data.push(dd);
        }

    })

    return [header, data];

}


 // Simple function to extract a single row from an array

 function getRow(matrix, col)
 {
     var column = [];
     for(var i = 0; i < matrix[0].length; i++){
        column.push(matrix[col][i]);
     }
     return column;
  }