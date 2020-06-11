#include <iostream>
#include "CameraApi.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

class CameraBuffer
{
public:
    CameraBuffer(const std::vector<uint8_t> &raw_buffer, size_t height, size_t width)
    {
        if(raw_buffer.size() != height * width * 3) {
            throw std::runtime_error("raw_buffer size does not match height and width");
        }
        _data = raw_buffer;
        _height = height;
        _width = width;
    }
    uint8_t *data() { return _data.data(); }
    int height() const { return _height; }
    int width() const { return _width; }

private:
    int _height;
    int _width;
    std::vector<uint8_t> _data;
};

CameraBuffer get_frame()
{

    int iCameraCounts = 4;
    int iStatus = -1;
    tSdkCameraDevInfo tCameraEnumList[4];
    int hCamera;
    tSdkCameraCapbility tCapability;
    tSdkFrameHead sFrameInfo;
    BYTE *pbyBuffer;
    tSdkImageResolution sImageSize;
    int i = 0;
    int num = 0;
    unsigned char *g_pRgbBuffer;

    std::vector<uint8_t> camera_buffer;

    CameraSdkInit(1);
    CameraEnumerateDevice(tCameraEnumList, &iCameraCounts);

    if (iCameraCounts == 0)
    {
        throw std::runtime_error("No cameras found");
    }

    iStatus = CameraInit(&tCameraEnumList[num], -1, -1, &hCamera);
    if (iStatus != CAMERA_STATUS_SUCCESS)
    {
        throw std::runtime_error("Camera init failed");
    }

    CameraGetCapability(hCamera, &tCapability);

    int image_buffer_size = tCapability.sResolutionRange.iHeightMax * tCapability.sResolutionRange.iWidthMax * 3;
    g_pRgbBuffer = (unsigned char *)malloc(image_buffer_size);

    CameraPlay(hCamera);

    CameraSetImageResolution(hCamera, &tCapability.pImageSizeDesc[0]);

    if (tCapability.sIspCapacity.bMonoSensor)
    {
        CameraSetIspOutFormat(hCamera, CAMERA_MEDIA_TYPE_MONO8);
    }
    else
    {
        CameraSetIspOutFormat(hCamera, CAMERA_MEDIA_TYPE_RGB8);
    }

    if (CameraGetImageBuffer(hCamera, &sFrameInfo, &pbyBuffer, 2000) == CAMERA_STATUS_SUCCESS)
    {
        CameraImageProcess(hCamera, pbyBuffer, g_pRgbBuffer, &sFrameInfo);

        camera_buffer.insert(camera_buffer.begin(), g_pRgbBuffer, g_pRgbBuffer + image_buffer_size);
        // camera_buffer.erase(camera_buffer.begin(), camera_buffer.end());

        CameraReleaseImageBuffer(hCamera, pbyBuffer);
    }
    else
    {
        throw std::runtime_error("Cameras capture timedout");
    }

    CameraUnInit(hCamera);
    free(g_pRgbBuffer);

    return CameraBuffer(camera_buffer, tCapability.sResolutionRange.iHeightMax, tCapability.sResolutionRange.iWidthMax);
}

int init() 
{
    int iCameraCounts = 4;
    int iStatus = -1;
    tSdkCameraDevInfo tCameraEnumList[4];
    int hCamera;
    tSdkCameraCapbility tCapability;
    int i = 0;
    int num = 0;

    CameraSdkInit(1);
    CameraEnumerateDevice(tCameraEnumList, &iCameraCounts);

    BOOL openStatus[4];
    CameraIsOpened(tCameraEnumList, openStatus);

    if (iCameraCounts == 0)
    {
        throw std::runtime_error("No cameras found");
    } 
    if (openStatus[num] == true){
        printf("Camera already initialised.");
        return 0;
    }

    iStatus = CameraInit(&tCameraEnumList[num], -1, -1, &hCamera);
    if (iStatus != CAMERA_STATUS_SUCCESS)
    {
        throw std::runtime_error("Camera init failed");
    }

    CameraGetCapability(hCamera, &tCapability);

    CameraPlay(hCamera);

    CameraSetImageResolution(hCamera, &tCapability.pImageSizeDesc[0]);

    if (tCapability.sIspCapacity.bMonoSensor)
    {
        CameraSetIspOutFormat(hCamera, CAMERA_MEDIA_TYPE_MONO8);
    }
    else
    {
        CameraSetIspOutFormat(hCamera, CAMERA_MEDIA_TYPE_RGB8);
    }

    return hCamera;
}

CameraBuffer capture(int hCamera)
{
    int iCameraCounts = 4;
    tSdkFrameHead sFrameInfo;
    BYTE *pbyBuffer;
    unsigned char *g_pRgbBuffer;
    std::vector<uint8_t> camera_buffer;

    if (CameraGetImageBuffer(hCamera, &sFrameInfo, &pbyBuffer, 2000) == CAMERA_STATUS_SUCCESS)
    {
        int image_buffer_size = sFrameInfo.iHeight * sFrameInfo.iWidth * 3;
        g_pRgbBuffer = (unsigned char *)malloc(image_buffer_size);

        CameraImageProcess(hCamera, pbyBuffer, g_pRgbBuffer, &sFrameInfo);

        camera_buffer.insert(camera_buffer.begin(), g_pRgbBuffer, g_pRgbBuffer + image_buffer_size);
        // camera_buffer.erase(camera_buffer.begin(), camera_buffer.end());

        CameraReleaseImageBuffer(hCamera, pbyBuffer);
    }
    else
    {
        throw std::runtime_error("Cameras capture timedout");
    }

    free(g_pRgbBuffer);

    return CameraBuffer(camera_buffer, sFrameInfo.iHeight, sFrameInfo.iWidth);
}

int close(int hCamera)
{
    if (CameraUnInit(hCamera) != CAMERA_STATUS_SUCCESS) {
        throw std::runtime_error("Camera UnInit failed");
    } else {
        return  0;
    }
}

PYBIND11_MODULE(_camera, m) {

    py::class_<CameraBuffer>(m, "CameraBuffer", py::buffer_protocol())
    .def_buffer([](CameraBuffer &buf) -> py::buffer_info {
        return py::buffer_info(
            buf.data(),                               /* Pointer to buffer */
            sizeof(uint8_t),                          /* Size of one scalar */
            py::format_descriptor<uint8_t>::format(), /* Python struct-style format descriptor */
            3,                                        /* Number of dimensions */
            {buf.height(), buf.width(), 3},           /* Buffer dimensions */
            {buf.width() * 3 * sizeof(uint8_t), 3 * sizeof(uint8_t), sizeof(uint8_t)} /* Strides (in bytes) for each index */
        );
    });

    // m.def("capture", &get_frame);
    m.def("init", &init);
    m.def("capture", &capture);
    m.def("close", &close);

}


// int main()
// {
//     std::vector<uint8_t> raw_buffer = get_frame();

//     CameraBuffer camera_buffer = CameraBuffer(raw_buffer);

//     std::cout << "length: " << camera_buffer.length() << std::endl;

//     return 0;
// }
