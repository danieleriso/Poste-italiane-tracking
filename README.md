# Poste-italiane-tracking
An unofficial Python API for Poste italiane shipment tracking service

## Example
```
trackingNumbers = ["AB01234CD", "EF56789GH"]
poste = PosteItaliane()
shipments = poste.track(trackingNumbers)

print poste
```
