# Telestream Cloud Flip Python SDK

This library provides a low-level interface to the REST API of Telestream Cloud, the online video encoding service.

## Requirements.

Python 2.7 and 3.4+

## Getting Started
### Initialize client

```python
import time
import telestream_cloud_flip
from telestream_cloud_flip.rest import ApiException
from pprint import pprint

api_instance = telestream_cloud_flip.FlipApi()
api_instance.api_client.configuration.api_key['X-Api-Key'] = '[API KEY]'

factory_id = '[FACTORY ID]'
```

### Upload video to flip service
```python
# Upload video
file_path = '/Users/rafalrozak/Downloads/panda.mp4'
profiles = 'h264'

extra_file_path = '/Users/rafalrozak/Downloads/sample.srt.txt'
extra_files = {
    'subtitles': [extra_file_path]
}

uploader = telestream_cloud_flip.Uploader(factory_id, api_instance, file_path, profiles, extra_files)
uploader.setup()
uploader.start()
pprint(uploader.status)
pprint(uploader.video_id)
```

### Create video from source URL
```python
# POST videos
createVideoBody = telestream_cloud_qc.CreateVideoBody(
    source_url="https://example.com/video.mp4", profiles="h264",
    subtitle_files=["https://example.com/subtitle.srt"]
)

try:
    video = api_instance.create_video(factoryId, createVideoBody)
    pprint(video)
except ApiException as e:
    print("Exception when calling FlipApi->create_video: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to *https://api.cloud.telestream.net/flip/3.1*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*FlipApi* | [**cancel_encoding**](docs/FlipApi.md#cancel_encoding) | **POST** /encodings/{id}/cancel.json | Cancels an Encoding.
*FlipApi* | [**copy_profile**](docs/FlipApi.md#copy_profile) | **POST** /profiles/{id}/copy.json | Copies a given Profile
*FlipApi* | [**create_encoding**](docs/FlipApi.md#create_encoding) | **POST** /encodings.json | Creates an Encoding
*FlipApi* | [**create_factory**](docs/FlipApi.md#create_factory) | **POST** /factories.json | Creates a new factory
*FlipApi* | [**create_profile**](docs/FlipApi.md#create_profile) | **POST** /profiles.json | Creates a Profile
*FlipApi* | [**create_video**](docs/FlipApi.md#create_video) | **POST** /videos.json | Creates a Video from a provided source_url.
*FlipApi* | [**create_workorder**](docs/FlipApi.md#create_workorder) | **POST** /workorders.json | Creates a Workorder.
*FlipApi* | [**delete_encoding**](docs/FlipApi.md#delete_encoding) | **DELETE** /encodings/{id}.json | Deletes an Encoding from both Telestream Cloud and your storage. Returns an information whether the operation was successful.
*FlipApi* | [**delete_profile**](docs/FlipApi.md#delete_profile) | **DELETE** /profiles/{id}.json | Deletes a given Profile
*FlipApi* | [**delete_video**](docs/FlipApi.md#delete_video) | **DELETE** /videos/{id}.json | Deletes a Video object.
*FlipApi* | [**delete_video_source**](docs/FlipApi.md#delete_video_source) | **DELETE** /videos/{id}/source.json | Delete a video&#39;s source file.
*FlipApi* | [**encoding**](docs/FlipApi.md#encoding) | **GET** /encodings/{id}.json | Returns an Encoding object.
*FlipApi* | [**encodings**](docs/FlipApi.md#encodings) | **GET** /encodings.json | Returns a list of Encoding objects
*FlipApi* | [**encodings_count**](docs/FlipApi.md#encodings_count) | **GET** /encodings/count.json | Returns a number of Encoding objects created using a given factory.
*FlipApi* | [**factories**](docs/FlipApi.md#factories) | **GET** /factories.json | Returns a collection of Factory objects.
*FlipApi* | [**factory**](docs/FlipApi.md#factory) | **GET** /factories/{id}.json | Returns a Factory object.
*FlipApi* | [**notifications**](docs/FlipApi.md#notifications) | **GET** /notifications.json | Returns a Factory&#39;s notification settings.
*FlipApi* | [**profile**](docs/FlipApi.md#profile) | **GET** /profiles/{id_or_name}.json | Returns a Profile object.
*FlipApi* | [**profile_encodings**](docs/FlipApi.md#profile_encodings) | **GET** /profiles/{id_or_name}/encodings.json | Returns a list of Encodings that belong to a Profile.
*FlipApi* | [**profiles**](docs/FlipApi.md#profiles) | **GET** /profiles.json | Returns a collection of Profile objects.
*FlipApi* | [**queued_videos**](docs/FlipApi.md#queued_videos) | **GET** /videos/queued.json | Returns a collection of Video objects queued for encoding.
*FlipApi* | [**resubmit_video**](docs/FlipApi.md#resubmit_video) | **POST** /videos/resubmit.json | Resubmits a video to encode.
*FlipApi* | [**retry_encoding**](docs/FlipApi.md#retry_encoding) | **POST** /encodings/{id}/retry.json | Retries a failed encoding.
*FlipApi* | [**signed_encoding_url**](docs/FlipApi.md#signed_encoding_url) | **GET** /encodings/{id}/signed-url.json | Returns a signed url pointing to an Encoding.
*FlipApi* | [**signed_encoding_urls**](docs/FlipApi.md#signed_encoding_urls) | **GET** /encodings/{id}/signed-urls.json | Returns a list of signed urls pointing to an Encoding&#39;s outputs.
*FlipApi* | [**signed_video_url**](docs/FlipApi.md#signed_video_url) | **GET** /videos/{id}/signed-url.json | Returns a signed url pointing to a Video.
*FlipApi* | [**toggle_factory_sync**](docs/FlipApi.md#toggle_factory_sync) | **POST** /factories/{id}/sync.json | Toggles synchronisation settings.
*FlipApi* | [**update_encoding**](docs/FlipApi.md#update_encoding) | **PUT** /encodings/{id}.json | Updates an Encoding
*FlipApi* | [**update_factory**](docs/FlipApi.md#update_factory) | **PATCH** /factories/{id}.json | Updates a Factory&#39;s settings. Returns a Factory object.
*FlipApi* | [**update_notifications**](docs/FlipApi.md#update_notifications) | **PUT** /notifications.json | Updates a Factory&#39;s notification settings.
*FlipApi* | [**update_profile**](docs/FlipApi.md#update_profile) | **PUT** /profiles/{id}.json | Updates a given Profile
*FlipApi* | [**upload_video**](docs/FlipApi.md#upload_video) | **POST** /videos/upload.json | Creates an upload session.
*FlipApi* | [**video**](docs/FlipApi.md#video) | **GET** /videos/{id}.json | Returns a Video object.
*FlipApi* | [**video_encodings**](docs/FlipApi.md#video_encodings) | **GET** /videos/{id}/encodings.json | Returns a list of Encodings that belong to a Video.
*FlipApi* | [**video_metadata**](docs/FlipApi.md#video_metadata) | **GET** /videos/{id}/metadata.json | Returns a Video&#39;s metadata
*FlipApi* | [**videos**](docs/FlipApi.md#videos) | **GET** /videos.json | Returns a collection of Video objects.
*FlipApi* | [**workflows**](docs/FlipApi.md#workflows) | **GET** /workflows.json | Returns a collection of Workflows that belong to a Factory.


## Documentation For Models

 - [CanceledResponse](docs/CanceledResponse.md)
 - [CloudNotificationSettings](docs/CloudNotificationSettings.md)
 - [CloudNotificationSettingsEvents](docs/CloudNotificationSettingsEvents.md)
 - [CopyProfileBody](docs/CopyProfileBody.md)
 - [CountResponse](docs/CountResponse.md)
 - [CreateEncodingBody](docs/CreateEncodingBody.md)
 - [CreateVideoBody](docs/CreateVideoBody.md)
 - [DeletedResponse](docs/DeletedResponse.md)
 - [Encoding](docs/Encoding.md)
 - [EncodingSignedUrl](docs/EncodingSignedUrl.md)
 - [EncodingSignedUrls](docs/EncodingSignedUrls.md)
 - [Error](docs/Error.md)
 - [ExtraFile](docs/ExtraFile.md)
 - [Factory](docs/Factory.md)
 - [FactoryBody](docs/FactoryBody.md)
 - [FactoryBodyStorageCredentialAttributes](docs/FactoryBodyStorageCredentialAttributes.md)
 - [FactorySync](docs/FactorySync.md)
 - [FactorySyncBody](docs/FactorySyncBody.md)
 - [PaginatedEncodingsCollection](docs/PaginatedEncodingsCollection.md)
 - [PaginatedFactoryCollection](docs/PaginatedFactoryCollection.md)
 - [PaginatedProfilesCollection](docs/PaginatedProfilesCollection.md)
 - [PaginatedVideoCollection](docs/PaginatedVideoCollection.md)
 - [PaginatedWorkflowsCollection](docs/PaginatedWorkflowsCollection.md)
 - [Profile](docs/Profile.md)
 - [ProfileBody](docs/ProfileBody.md)
 - [ResubmitVideoBody](docs/ResubmitVideoBody.md)
 - [RetriedResponse](docs/RetriedResponse.md)
 - [SignedVideoUrl](docs/SignedVideoUrl.md)
 - [UpdateEncodingBody](docs/UpdateEncodingBody.md)
 - [UploadSession](docs/UploadSession.md)
 - [Video](docs/Video.md)
 - [VideoMetadata](docs/VideoMetadata.md)
 - [VideoUploadBody](docs/VideoUploadBody.md)


## Documentation For Authorization


## api_key

- **Type**: API key
- **API key parameter name**: X-Api-Key
- **Location**: HTTP header


## Author

cloudsupport@telestream.net

