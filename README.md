# PyTfL

### A Python library for easy and intuitive maniplulation of TfL's API.

----------

### Usage

To get things up and running, you'll need to:
 - [Register](https://api-portal.tfl.gov.uk) an app with TfL
    - You'll need to create a product subscription under `Products -> <product name>`
        - At the time of writing, the only product available is `500 Requests per min`
 - Copy `PyTfL.conf.template` to a `PyTfL.conf` file, and fill in your app's details
    - TfL's jargon for describing these keys appears to be inconsistent: 
        - "Primary key" corresponds to `app_id`
        - "Secondary key" to `app_key`
 - Point the app to where this file is located by either:
    - Setting the `PYTFL_CONFIG` environment variable to your `PyTfL.cong`'s path
    - Being in the same directory as your `PyTfL.conf` file 
 
----------

#### Up+coming -
TfL's tube network.

##### TODO:

- [ ] TubeLines class
    - [x] Basic TubeLines class
    - [x] Integrate TubeStations into TubeLines
    - [x] Integrate TubeRoutes into TubeLines
    - [ ] Tidy up the initialisation of these classes in the DAO, Currently takes too long (~30 seconds without caching on TfL's side, ~12 seconds with).
- [ ] TubeNetwork class
    - [x] Rationalise what this is supposed to mean. May need to move much of the functionality found here into a DAO.
    - [ ] Create whole network and measure how long this takes. Optimise if necessary.
- [ ] TubeStation class
    - [x] Basic TubeStation class
    - [ ] Make use of additionaProperties key - could organised them by the 'category' key.
    - [ ] Make use of children key. This can be postponed until other transport types (particularly bus) are incorporated.
    - [ ] Entrances (NaptanMetroEntrance)
    - [ ] Platforms (NaptanMetroPlatform)
    - [ ] Concourses (NaptanMetroAccessArea)
- [x] TubeRoute class
    - [x] Basic TubeRoute class

## Further Information -

- Government [**documents**](https://www.gov.uk/government/publications/national-public-transport-access-node-schema) on understanding NaPTAN

