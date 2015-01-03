window.addEventListener('storage', onStoreEdit);
var oAuthWindow = null;
function startLogin()
{
    oAuthWindow = window.open('/oauth/login', '_blank', 'menubar=0,status=0')
}

function onStoreEdit(e)
{
    if(e.key == 'oauth-login')
    {
        if(e.newValue == 'true')
        {
            window.localStorage.removeItem('oauth-login');
            onLogin();
        }
    }
}

function onLogin()
{
    window.location.href = '/home';
}