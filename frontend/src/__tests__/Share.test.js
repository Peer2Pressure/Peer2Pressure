import React from 'react';
import {render, screen, fireEvent, cleanup } from '@testing-library/react'
import '@testing-library/jest-dom'
import Share from '../components/share/Share';

afterEach(cleanup);
global.URL.createObjectURL = jest.fn();

test("share should have right parts", async () => {
    render(<Share/>)
    await screen.findByRole("button")
    expect(screen.getByRole("button")).toHaveTextContent("Post")
})

test("you can upload images", async () => {
    const { getByLabelText, getByAltText } = render(<Share />);
    const inputEl = getByLabelText("Upload a Photo");

    const file = new File(["dummy image"], "an_image.png", {
        type: "image/png"
    });

    Object.defineProperty(inputEl, "files", {
        value: [file]
    });

    fireEvent.change(inputEl);
    getByAltText(file)
})

test("you can't upload non images", async () => {
    const { getByLabelText, getByText } = render(<Share />);
    const inputEl = getByLabelText("Upload a Photo");

    const file = new File(["dummy pdf"], "not_an_image.pdf", {
        type: "application/pdf"
    });

    Object.defineProperty(inputEl, "files", {
        value: [file]
    });

    fireEvent.change(inputEl);
    getByText("only jpeg and png accepted")
})