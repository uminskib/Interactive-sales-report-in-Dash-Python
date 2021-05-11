
import dash
import dash_auth
from log_in import user_password
#inicjalizacja aplikacji dash
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
#Logowanie do strony
auth = dash_auth.BasicAuth(
    app,
    user_password
)
app.title ='Raport' 
server = app.server
#instrukcja pozwalająca na używanie odwołań w kilku plikach
app.config.suppress_callback_exceptions=True

