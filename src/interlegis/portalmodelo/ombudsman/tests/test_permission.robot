*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${title_selector} =  input#form-widgets-IDublinCore-title
${description_selector} =  textarea#form-widgets-IDublinCore-description

*** Test cases ***

Test Workflow
    Enable Autologin as  Site Administrator
    Go to Homepage
    Create Ombuds Office
    Workflow Publish

    Disable Autologin
    Enable Autologin as  Contributor
    Create AdminClaim

    Disable Autologin
    Go to ombuds_office
    View AnonymousClaim

*** Keywords ***

Go to ombuds_office
    Go to   ${PLONE_URL}/ombuds-office
    Wait until location is  ${PLONE_URL}/ombuds-office

Click Add Ombuds Office
    Open Add New Menu
    Click Link  css=a#ombudsoffice
    Page Should Contain  Ombuds Office

Click Add Claim
    Open Add New Menu
    Click Link  css=a#claim
    Page Should Contain  Add Claim

Create Ombuds Office
    [documentation]  Fill the form to create an Ombuds Office; note there's
    ...              a strange behavior on the Data Grid: after filling
    ...              the responsible field, it adds a new row and the id
    ...              changes unexpectedly to "0" instead of "AA"
    Click Add Ombuds Office
    Input Text  css=#form-widgets-title  Ombuds Office
    Input Text  css=#form-widgets-claim_types-0-widgets-claim_type  Type1
    Input Text  css=#form-widgets-areas-0-widgets-area  Area1
    Input Text  css=#form-widgets-areas-0-widgets-responsible  Deep Thought
    Input Text  css=#form-widgets-areas-0-widgets-email  foo@bar.com
    Click Button  Save
    Page Should Contain  Item created

View AnonymousClaim
    Click Link  Don't Panic
    Page Should Contain  I want to learn the Answer to the Ultimate Question of Life, the Universe, and Everything
    Page Should Not Contain  Marvim
    Page Should Not Contain  marvim@galaxy.com
    Page Should Not Contain  04242-042

Create AdminClaim
    Click Add Claim
    Input Text  css=#form-widgets-title  Don't Panic
    Input Text  css=#form-widgets-description  I want to learn the Answer to the Ultimate Question of Life, the Universe, and Everything
    Input Text  css=#form-widgets-name  Marvim
    Input Text  css=#form-widgets-email  marvim@galaxy.com
    Input Text  css=#form-widgets-address  Rua Comendador da Terra, 42
    Input Text  css=#form-widgets-postal_code  04242-042
    Input Text  css=#form-widgets-city  Caxias
    Select From List  css=#form-widgets-state  RS
    Click Button  Save
    Page Should Contain  Item created
    Page Should Contain  Marvim
    Page Should Contain  marvim@galaxy.com
    Page Should Contain  04242-042
