export default function AboutPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:px-8">
      <h1 className="text-3xl font-bold">About the Lab</h1>
      <p className="mt-4 text-slate-600 dark:text-slate-300">
        Image Processing Lab is an interactive laboratory built around the Image Processing Lab
        course (N-PECCS502P). Every practical you see here — from image fundamentals and
        geometric transformations to enhancement, filtering, restoration, compression,
        morphology, and object detection — runs on a real Python/OpenCV backend rather than
        pre-baked demo images.
      </p>
      <p className="mt-4 text-slate-600 dark:text-slate-300">
        The goal is simple: let students read the theory, see the reference implementation, run
        the actual algorithm on their own image, and generate a properly formatted practical
        report — all in one place, reusable by current and future students.
      </p>
    </div>
  );
}
