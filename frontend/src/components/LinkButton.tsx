import { LinkButtonProps } from "@/types";
import Link from "next/link";

export default function LinkButton({ title, href, style }: LinkButtonProps) {
  return (
    <Link href={href}>
      <button type="button" className={style}>
        {title}
      </button>
    </Link>
  );
}
