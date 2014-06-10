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
    Create Claim

*** Keywords ***

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
    Input Text  css=#form-widgets-claim_types-AA-widgets-claim_type  Type1
    Input Text  css=#form-widgets-areas-AA-widgets-area  Area1
    Input Text  css=#form-widgets-areas-AA-widgets-responsible  Deep Thought
    Input Text  css=#form-widgets-areas-0-widgets-email  foo@bar.com
    Click Button  Save
    Page Should Contain  Item created

Create Claim
    Click Add Claim
    Input Text  css=#form-widgets-title  Don't Panic
    Input Text  css=#form-widgets-description  I want to learn the Answer to the Ultimate Question of Life, the Universe, and Everything
    Input Text  css=#form-widgets-name  Zé Ninguém
    Input Text  css=#form-widgets-email  foo@bar.com
    Input Text  css=#form-widgets-address  Rua Comendador Roberto Ugolini, 20
    Input Text  css=#form-widgets-postal_code  03125-010
    Input Text  css=#form-widgets-city  Mooca
    Select From List  css=#form-widgets-state  SP
    Click Button  Save
    Page Should Contain  Item created

Create Response
    [arguments]  ${answer}
    Click Add Response
    Input Text  css=#form-widgets-text  ${answer}
    Click Button  Save
    Page Should Contain  Item created
