import React from 'react';
import {render, screen, fireEvent, cleanup, findByText } from '@testing-library/react'
import '@testing-library/jest-dom'
import ProfileSetting from '../components/profileSetting/ProfileSetting';

afterEach(cleanup);

test("should have the right parts", async () => {
    render(<ProfileSetting/>)
    await screen.findByText("Username")
    await screen.findByText("Full Name")
    await screen.findByText("Email")
    await screen.findByText("Password")
})