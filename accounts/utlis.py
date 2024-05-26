
def detectuser(user):
    if user.role==1:
        redirectUrl='vendordashboard'
        return redirectUrl
    elif user.role==2:
        redirectUrl='cusdashboard'
        return redirectUrl

    elif user.role == None and user.is_superadmin:
        redirectUrl ='/admin'
        return redirectUrl