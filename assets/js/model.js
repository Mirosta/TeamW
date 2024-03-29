var apiUrl = "/api/";
var createUrl = "/add";
var updateUrl = "/update";
var deleteUrl = "/remove";
var getUrl = "/{{id}}";

function Model(modelUrl, idOrObj)
{
    if(!idOrObj) this.id = null; //No id or object given
    else if(typeof idOrObj === "object") //Object given, copy properties from it
    {
        for(var key in idOrObj)
        {
            if(idOrObj.hasOwnProperty(key)) this[key] = idOrObj[key];
        }
    }
    else this.id = idOrObj; //ID given, just set the id

    this.modelUrl = modelUrl;

    var thisObj = this;

    this.create = function(callback) //Callback is same as util.js apiPost function
    {
        var url = apiUrl + thisObj.modelUrl + createUrl;
        //Create object in DB
        apiPost(url, stripNonSerializableFields(thisObj, ['modelUrl', 'readOnly']), callback);
    };
    this.update = function(callback) //Callback is same as util.js apiPost function
    {
        var url = apiUrl + thisObj.modelUrl + updateUrl;
        //Update object in DB
        apiPost(url, stripNonSerializableFields(thisObj, ['modelUrl', 'readOnly']), callback);
    };
    this.remove = function(callback) //Callback is same as util.js apiPost function
    {
        var url = apiUrl + thisObj.modelUrl + deleteUrl;
        //Remove object in DB
        apiPost(url, stripNonSerializableFields(thisObj, ['modelUrl', 'readOnly']), callback);
    };
    this.getFields = function()
    {
        var retArr = [];
        var strippedThis = stripNonSerializableFields(thisObj, ['modelUrl', 'readOnly']);
        for(var key in strippedThis)
        {
            if(typeof strippedThis[key] !== "function")
            {
                retArr.push(key);
            }
        }

        for(var key in thisObj.readOnly)
        {
            if(typeof thisObj.readOnly[key] !== "function")
            {
                retArr.push("readOnly." + key);
            }
        }

        return retArr;
    };
}

function ModelClass(modelUrl)
{
    this.modelUrl = modelUrl;
    models[this.modelUrl] = this;
    var getAllUrl = "/";
    var allResultsProperty = "results";
    var thisObj = this;

    this.get = function(id, callback) //Callback is same as util.js apiGet function
    {
        var url = apiUrl + thisObj.modelUrl + processTemplate(getUrl, {id: id}); //Get url is a template, pass the current model obj into the template function
        //Get object from DB
        apiGet(url,
            function(success, data)
            {
                if(success)
                {
                    if(callback) callback(success, new Model(thisObj.modelUrl, data));
                }
                else
                {
                    if(callback) callback(success, data);
                }
            }
        );
    };
    this.getAll = function(callback, count, offset, sortBy) //Callback is of format function(boolean success, (string | array) errorOrResults)
    {
        var parameters = "";
        var paramParts = [{name: "count", value: count}, {name: "offset", value: offset}, {name: "sortBy", value: sortBy}];
        var sep = "?";

        for(var i =0; i < paramParts.length; i++)
        {
            if(paramParts[i].value)
            {
                parameters += sep;
                parameters += paramParts[i].name + "=" + paramParts[i].value;
                sep = "&";
            }
        }

        var url = apiUrl + thisObj.modelUrl + getAllUrl + parameters;
        //Get object from DB
        apiGet(url,
            function (success, data)
            {
                if(success)
                {
                    var all = [];
                    for(var i = 0; i < data[allResultsProperty].length; i++)
                    {
                        all.push(new Model(thisObj.modelUrl, data[allResultsProperty][i]));
                    }
                    if(callback) callback(success, all);
                }
                else
                {
                    if(callback) callback(success, data);
                }
            });
    };
    this.newInstance = function(object) //Object should contain the fields to set in the model object
    {
        return new Model(thisObj.modelUrl, object);
    };
}

//Create a ModelClass for groups, you can get group objects that extend Model using the .get or .getAll methods
var models = {};

var groups = new ModelClass("groups");

var friends = new ModelClass("friends");

var payments = new ModelClass("payments");

var user = new ModelClass("user");

var debts = new ModelClass("debts");

var notifications = new ModelClass("notifications");

var friendRequests = new ModelClass("friends/request")

//Model objects have .update, .create and .remove methods
/*
Example: Get all groups

var allGroups = groups.getAll(
    function(success, data)
    {
        if(success)
        {
            console.log('Got all groups:');
            console.log(data);
        }
        else
        {
            console.log('Error when getting groups: ' + data);
        }
    }
);
/*
//Example: Get group with id 1
//NOTE: Objects don't necessarily have integer ids, they can be strings
/*

var group1 = null;
groups.get("1",
    function(success, data)
    {
        if(success)
        {
            console.log('Got group 1:');
            console.log(data);
            group1 = data;
        }
        else
        {
            console.log('Error when getting group 1: ' + data);
        }
    }
);
*/
//Example: Update name of group 1
/*
group1.name = "Broadlands Road";
group1.update();
*/
//Example: Remove group 1
//group1.remove();

//Example: Create a new group in the DB, with no users
/*
var newGroup = groups.newInstance({"name": "New Group"}); //Properties can be passed in when creating a new group
newGroup.users = []; //Or later by setting the properties directly
newGroup.create();
*/
