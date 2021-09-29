## Part 1: The data

The data that is stored inside this jwt is
```
{
    "u_id": "12345"
}
```

## Part 2: Justification about tampering

Yes the jwt `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTIzNDUifQ.lBTAPFU1xxDAi2Vrusfo67ypBai0vBr6O7KOt6CJf1s`,
has been modifed which can be determined by comparing it to the jwt created by encoding the data from above with the secret `comp1531`
which produces `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTIzNDUifQ.MByA9mwoKP56SQUi1S-bjzNpRsvHWS7oEIewq-8qVuU`.